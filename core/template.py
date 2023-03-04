from functools import reduce
from hashlib import md5
from jsonpath import jsonpath
from jsonpath_ng.parser import JsonPathParser
from tools.funclib import get_func_lib
import json
import re
import time

from tools.utils.utils import extract_by_jsonpath, quotation_marks


class Template:

    def __init__(self, context, functions, params, variable_start_string='{{', variable_end_string='}}', function_prefix='@', param_prefix='$'):
        self.param_prefix = param_prefix
        self.data = None
        self.context = context  # 关联参数
        self.params = params    # 公共参数
        self.variable_start_string = variable_start_string
        self.variable_end_string = variable_end_string
        self.function_prefix = function_prefix
        self.param_prefix = param_prefix
        self.stack = list()
        # 动态存储接口的请求信息 以便渲染
        self.request_path = None
        self.request_headers = None
        self.request_query = None
        self.request_body = None
        self.func_lib = get_func_lib(functions, self.context, self.params)
        self.bytes_map = dict()
        self.parser = JsonPathParser()

    def init(self, data):
        self.data = json.dumps(data, ensure_ascii=False)
        self.stack.clear()
        self.bytes_map.clear()

    def set_help_data(self, path: str, headers: dict, query: dict, body: dict):
        self.request_path = path
        self.request_headers = headers
        self.request_query = query
        self.request_body = body

    def render(self):
        start_stack = list()
        start_length = len(self.variable_start_string)
        end_length = len(self.variable_end_string)
        top = 0
        flag = False
        for cur in range(len(self.data)):
            self.stack.append(self.data[cur])
            top += 1
            if flag:
                self.stack.pop()
                top -= 1
                flag = False
                continue
            if reduce(lambda x, y: x + y, self.stack[-start_length:]) == self.variable_start_string:
                start_stack.append(top - start_length)
            if reduce(lambda x, y: x + y, self.stack[-end_length:]) == self.variable_end_string:
                if len(start_stack) == 0:
                    continue
                recent = start_stack.pop()
                tmp = ''
                for _ in range(top - recent):
                    tmp += self.stack.pop()
                    top -= 1
                if self.stack[-1] == '"' and self.data[cur + 1] == '"':
                    self.stack.pop()
                    top -= 1
                    flag = True
                else:
                    flag = False
                tmp = tmp[::-1]
                key = tmp[start_length:-end_length].strip()
                if key in self.context:
                    value = self.context.get(key)
                elif key.startswith(self.param_prefix) and key[1:] in self.params:
                    value = self.params.get(key[1:])
                elif key.startswith(self.function_prefix):
                    name_args = self.split_func(key, self.function_prefix)
                    name_args = [_ for _ in map(self.replace_param, name_args)]
                    value = self.func_lib(name_args[0], *name_args[1:])
                else:
                    raise NotExistedVariableOrFunctionError('不存在的公共参数、关联变量或取值函数: {}'.format(key))

                if not flag and type(value) is str:
                    final_value = value
                elif isinstance(value, bytes):
                    final_value = self._bytes_save(value, flag)
                elif isinstance(value, list):
                    final_value = list()
                    for list_item in value:
                        if isinstance(list_item, bytes):
                            final_value.append(self._bytes_save(list_item, False))
                        else:
                            final_value.append(list_item)
                    final_value = json.dumps(final_value)
                else:
                    final_value = json.dumps(value)
                for s in final_value:
                    self.stack.append(s)
                    top += 1
        res = json.loads(reduce(lambda x, y: x + y, self.stack))

        if len(self.bytes_map) > 0:
            pattern = r'#\{(bytes_\w+_\d+?)\}'
            if isinstance(res, str):
                bytes_value = self._bytes_slove(res, pattern)
                if bytes_value is not None:
                    res = bytes_value
            elif isinstance(res, dict) or isinstance(res, list):
                for i, j in zip(jsonpath(res, '$..'), jsonpath(res, '$..', result_type='PATH')):
                    if isinstance(i, str):
                        bytes_value = self._bytes_slove(i, pattern)
                        if bytes_value is not None:
                            expression = self.parser.parse(j)
                            expression.update(res, bytes_value)
        return res

    def _bytes_save(self, value, flag):
        bytes_map_key = 'bytes_{}_{}'.format(md5(value).hexdigest(), int(time.time() * 1000000000))
        self.bytes_map[bytes_map_key] = value
        change_value = '#{%s}' % bytes_map_key
        if flag:
            final_value = json.dumps(change_value)
        else:
            final_value = change_value
        return final_value

    def _bytes_slove(self, s, pattern):
        search_result = re.search(pattern, s)
        if search_result is not None:
            expr = search_result.group(1)
            return self.bytes_map[expr]

    def replace_param(self, param):
        if not isinstance(param, str):
            return param
        search_result = re.search(r'#\{(.*?)\}', param)
        if search_result is not None:
            expr = search_result.group(1).strip()
            if expr.lower() == '_request_path':
                return self.request_path
            elif expr.lower() == '_request_header':
                return self.request_headers
            elif expr.lower() == '_request_body':
                return self.request_body
            elif expr.lower() == '_request_query':
                return self.request_query
            elif expr.startswith('bytes_'):
                return self.bytes_map[expr]
            else:
                if not expr.startswith('$'):
                    expr = '$.' + expr
                return extract_by_jsonpath(self.request_body, expr)
        else:
            return param

    def split_func(self, statement: str, flag: 'str' = '@'):
        pattern = flag + r'([_a-zA-Z][_a-zA-Z0-9]*)(\(.*?\))?'
        m = re.match(pattern, statement)
        result = list()
        if m is not None:
            name, args = m.groups()
            result.append(name)
            if args is not None and args != '()':
                argList = [arg.strip() for arg in args[1:-1].split(',')]
                argList_length = len(argList)
                if not (argList_length == 1 and len(argList[0]) == 0):
                    if name not in self.func_lib.func_param:
                        for i in range(argList_length):
                            result.append(argList[i])
                    else:
                        type_list = self.func_lib.func_param[name]
                        j = 0
                        for i in range(len(type_list)):
                            if j >= argList_length:
                                break
                            if type_list[i] is str:
                                result.append(quotation_marks(argList[j]))
                                j += 1
                            elif type_list[i] is int:
                                result.append(int(argList[j]))
                                j += 1
                            elif type_list[i] is float:
                                result.append(float(argList[j]))
                                j += 1
                            elif type_list[i] is bool:
                                result.append(False if argList[j].lower() == 'false' else True)
                                j += 1
                            elif type_list[i] is dict:
                                j, r = self.concat(j, argList, '}')
                                result.append(r)
                            elif type_list[i] is list:
                                j, r = self.concat(j, argList, ']')
                                result.append(r)
                            elif type_list[i] is bytes:
                                result.append(argList[j])
                                j += 1
                            elif type_list[i] is None:
                                result.append(argList[j])
                                j += 1
                            else:
                                raise SplitFunctionError('函数{}第{}个参数类型错误: {}'.format(name, i + 1, type_list[i]))
            return result
        else:
            raise SplitFunctionError('函数错误: {}'.format(statement))

    @staticmethod
    def concat(start: int, arg_list: list, terminal_char: str):
        end = -1
        length = len(arg_list)
        for i in range(start, length):
            if terminal_char in arg_list[i] and i > end:
                end = i
        s = reduce(lambda x, y: x + ',' + y, arg_list[start:end + 1])
        r = json.loads(quotation_marks(s))
        if isinstance(r, str):
            r = json.loads(r)
        return end + 1, r


class NotExistedVariableOrFunctionError(Exception):
    """不存在的应用变量或者函数"""


class SplitFunctionError(Exception):
    """函数处理错误"""
