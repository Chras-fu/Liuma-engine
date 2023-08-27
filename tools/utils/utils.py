import json
import re
from urllib.parse import quote
import jsonpath
import copy


def extract_by_jsonpath(data: (dict, str), expression: str):
    if not isinstance(data, dict):
        raise ExtractValueError('被提取的值不是json, 不支持jsonpath')
    value = jsonpath.jsonpath(data, expression)
    if value:
        return value[0] if len(value) == 1 else value
    else:
        raise ExtractValueError('jsonpath表达式错误: {}'.format(expression))


def extract_by_regex(data: (dict, str), pattern: str):
    if isinstance(data, dict):
        content = json.dumps(data, ensure_ascii=False)
    else:
        content = data
    result = re.findall(pattern, content)
    if len(result) > 0:
        return result[0] if len(result) == 1 else result
    else:
        raise ExtractValueError("正则表达式匹配失败: {}".format(pattern))


def quotation_marks(s):
    if s[0] in ["'", '"', b'\xe2\x80\x98'.decode('utf-8'), b'\xe2\x80\x99'.decode('utf-8'),
                b'\xe2\x80\x9c'.decode('utf-8'), b'\xe2\x80\x9d'.decode('utf-8')]:
        before = 1
    elif s[0:2] in ["\\'", '\\"']:
        before = 2
    else:
        return s
    # 后引号, 先判断转义的，在判断单个引号
    if s[-2:] in ["\\'", '\\"']:
        after = -2
    elif s[-1] in ["'", '"', b'\xe2\x80\x98'.decode('utf-8'), b'\xe2\x80\x99'.decode('utf-8'),
                   b'\xe2\x80\x9c'.decode('utf-8'), b'\xe2\x80\x9d'.decode('utf-8')]:
        after = -1
    else:
        return s
    return s[before:after]


def url_join(host: str, path: str):
    url = host if host.endswith('/') else host + '/'
    api = path[1:] if path.startswith('/') else path
    return url + api


def proxies_join(proxies: dict):
    if 'url' not in proxies or proxies['url'] is None or len(proxies['url']) == 0:
        raise ProxiesError("未设置代理网址")
    if not proxies['url'].startswith('http'):
        proxies['url'] = 'http://' + proxies['url']
    if 'username' not in proxies or proxies['username'] is None or len(proxies['username']) == 0:
        proxies['username'] = None
    else:
        proxies['username'] = quote(proxies['username'], safe='')
    if 'password' not in proxies or proxies['password'] is None or len(proxies['password']) == 0:
        proxies['password'] = None
    else:
        proxies['password'] = quote(proxies['password'], safe='')
    scheme = proxies['url'].split(':')[0]
    if proxies['username'] is not None and proxies['password'] is not None:
        pre, suf = proxies['url'].split('//', maxsplit=1)
        url = '{}//{}:{}@{}'.format(pre, proxies['username'], proxies['password'], suf)
        return {scheme: url}
    elif proxies['username'] is None and proxies['password'] is None:
        return {scheme: proxies['url']}
    else:
        raise ProxiesError("未设置代理账号或密码")


def extract(name: str, data: (dict, str), expression: str):
    if name == 'jsonpath':
        return extract_by_jsonpath(data, expression)
    elif name == 'regular':
        return extract_by_regex(data, expression)
    else:
        raise ExtractValueError("未定义提取函数: {}".format(name))


def get_case_message(data):
    if isinstance(data, dict):
        return data
    else:
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            with open(data, 'rb') as f:
                return json.load(f)


def handle_operation_data(data_type, data_value):
    try:
        if data_type == "JSONObject":
            data_value = eval(data_value)
        elif data_type == "JSONArray":
            data_value = eval(data_value)
        elif data_type == "Boolean":
            if data_value.lower() == "true":
                data_value = True
            else:
                data_value = False
        elif data_type == "Int":
            data_value = int(data_value)
        elif data_type == "Float":
            data_value = float(data_value)
        elif data_type == "Number":
            data_value = float(data_value) if "." in data_value else int(data_value)
        else:
            data_value = data_value
    except:
        pass
    return data_value


def handle_params_data(params):
    result = {}
    for key, item in params.items():
        data_type = item["type"]
        data_value = item["value"]
        try:
            if data_type == "JSONObject":
                data_value = eval(data_value)
            elif data_type == "JSONArray":
                data_value = eval(data_value)
            elif data_type == "Boolean":
                if data_value.lower() == "true":
                    data_value = True
                else:
                    data_value = False
            elif data_type == "Int":
                data_value = int(data_value)
            elif data_type == "Float":
                data_value = float(data_value)
        except:
            pass
        result[key] = data_value
    return result


def handle_form_data(form):
    form_data = {}
    form_file = {}
    for item in form:
        try:
            if item["type"] == "File":
                form_file[item["name"]] = "{{@loadfile(%s)}}" % item["value"]
            elif item["type"] == "JSONObject":
                form_data[item["name"]] = eval(item["value"])
            elif item["type"] == "JSONArray":
                form_data[item["name"]] = eval(item["value"])
            elif item["type"] == "Boolean":
                if item["value"].lower() == 'true':
                    form_data[item["name"]] = True
                else:
                    form_data[item["name"]] = False
            elif item["type"] == "Int":
                form_data[item["name"]] = int(item["value"])
            elif item["type"] == "Float":
                form_data[item["name"]] = float(item["value"])
            else:
                form_data[item["name"]] = item["value"]
        except:
            form_data[item["name"]] = item["value"]
    return form_data, form_file


def handle_files(files):
    body_files = []
    for item in files:
        file_name = item["name"]
        file_value = "{{@loadfile(%s)}}" % item["id"]
        body_files.append(("file", (file_name, file_value)))
    return body_files


def json_to_path(data):
    queue = [("_REQUEST_BODY", data)]
    fina = {}
    while len(queue) != 0:
        (path, tar) = queue.pop()
        if len(tar) == 0:
            fina["%s" % path] = tar
        if isinstance(tar, dict):
            for key, value in tar.items():
                try:
                    if key.isdigit():
                        key = "'%s'" % str(key)
                except:
                    key = "'%s'" % str(key)
                if isinstance(value, dict) or isinstance(value, list):
                    queue.append(("%s.%s" % (path, key), value))
                else:
                    fina["%s.%s" % (path, key)] = value
        else:
            for index, value in enumerate(tar):
                if isinstance(value, dict) or isinstance(value, list):
                    queue.append(("%s[%d]" % (path, index), value))
                else:
                    fina["%s[%d]" % (path, index)] = value
    return fina


def relate_sort(data, data_from):
    not_relate_list = []
    relate_list = []
    for key, value in data.items():
        if "#{" in str(value):
            relate_list.append((key.replace("_REQUEST_BODY", "$"), value))
        else:
            not_relate_list.append((key.replace("_REQUEST_BODY", "$"), value))
    copy_list = copy.deepcopy(relate_list)
    sorted_list = []
    for index in range(len(relate_list)):
        for (key, value) in copy_list:
            for (com_key, com_value) in copy_list:
                if com_key[0:2] == "$.":
                    json_path = com_key[2:]
                else:
                    json_path = com_key[1:]
                if json_path in str(value) and com_key != key:
                    break
            else:
                sorted_list.append((key, value))
                copy_list.remove((key, value))
                break
    for (key, value) in sorted_list:
        if data_from == "query":
            sign = "#{_request_query}"
        elif data_from == "headers":
            sign = "#{_request_header}"
        else:
            sign = "#{_request_body}"
        if sign in str(value).lower():
            sorted_list.remove((key, value))
            sorted_list.append((key, value))
            break
    return not_relate_list + sorted_list


def get_json_relation(data: dict, data_from: str):
    return relate_sort(json_to_path(data), data_from)


class ExtractValueError(Exception):
    """提取值失败"""


class ProxiesError(Exception):
    """错误代理"""
