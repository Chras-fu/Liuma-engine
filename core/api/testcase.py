import re
import sys

from core.api.collector import ApiRequestCollector
from core.template import Template
from core.api.teststep import ApiTestStep, log_msg
from jsonpath_ng.parser import JsonPathParser

from tools.utils.utils import get_case_message, get_json_relation, handle_params_data


class ApiTestCase:

    def __init__(self, test):
        self.test = test
        self.case_message = get_case_message(test.test_data)
        self.session = test.session
        self.context = test.context
        self.id = self.case_message['caseId']
        self.name = self.case_message['caseName']
        setattr(test, 'test_case_name', self.case_message['caseName'])
        setattr(test, 'test_case_desc', self.case_message['comment'])
        self.functions = self.case_message['functions']
        self.params = handle_params_data(self.case_message['params'])
        self.template = Template(self.context, self.functions, self.params)
        self.json_path_parser = JsonPathParser()
        self.comp = re.compile(r"\{\{.*?\}\}")

    def execute(self):
        """用例执行入口函数"""
        if self.case_message['apiList'] is None:
            raise RuntimeError("无法获取API相关数据, 请重试!!!")
        self._loop(self.case_message['apiList'], "root")

    def _loop(self, api_list, loop_id, index=0):
        """循环执行"""
        while index < len(api_list):
            api_data = api_list[index]
            index += 1
            # 定义事务
            self.test.defineTrans(api_data['apiId'], api_data['apiName'], api_data['path'])
            # 按json模板中的接口顺序收集ApiTestStep实例
            collector = ApiRequestCollector()
            collector.collect(api_data)
            step = ApiTestStep(self.test, self.session, collector, self.context, self.params)
            try:
                # 渲染逻辑控制器
                self._render_controller(step)
                # 循环控制器
                if step.collector.controller["loopExec"] is not None and step.collector.controller["loopExec"] != "{}" \
                        and not (loop_id != "root" and index == 1):
                    # 非根循环 且并非循环第一个接口时才执行循环 从而避免循环套循环情况下的死循环
                    loop = step.loop_exec()
                    self.test.deleteTrans(-1)   # 循环前删除本次接口事务定义
                    for i in range(loop[1]):  # 本次循环次数
                        self.context[loop[0]] = i+1  # 给循环索引赋值第几次循环 母循环和子循环的索引名不应一样
                        _api_list = api_list[index-1: (index+loop[2]-1)]
                        self._loop(_api_list, api_data["apiId"])
                    index = index + loop[2] - 1  # 跳过本次循环中执行的接口
                    continue    # 母循环最后一个接口索引必须超过子循环的最后一个接口索引 否则超过母循环的接口无法执行
                # 条件控制器
                if step.collector.controller["whetherExec"] is not None:
                    print(step.collector.controller["whetherExec"])
                    msg = step.judge_condition()
                    if msg is not True:
                        self.test.updateTransStatus(3)   # 任意条件不满足 跳过执行
                        self.test.debugLog('[{}][{}]接口执行条件为否: {}'.format(
                            step.collector.apiId, step.collector.apiName, msg))
                        continue
                # 执行前置脚本
                if step.collector.controller["preScript"] is not None:
                    step.exec_script(step.collector.controller["preScript"])
                # 渲染主体
                self._render_content(step)
                # 执行step, 接口参数移除，接口请求，接口响应，断言操作，依赖参数提取
                step.execute()
                # 执行后置脚本
                if step.collector.controller["postScript"] is not None:
                    step.exec_script(step.collector.controller["postScript"])
                # 检查step的断言结果
                if step.assert_result['result']:
                    self.test.debugLog('[{}][{}]接口断言成功: {}'.format(step.collector.apiId,
                                                                   step.collector.apiName,
                                                                   log_msg(step.assert_result['checkMessages'])))
                else:
                    self.test.errorLog('[{}][{}]接口断言失败: {}'.format(step.collector.apiId,
                                                                   step.collector.apiName,
                                                                   log_msg(step.assert_result['checkMessages'])))
                    raise AssertionError(log_msg(step.assert_result['checkMessages']))
            except Exception as e:
                error_info = sys.exc_info()
                if step.collector.controller["errorContinue"].lower() == "true":
                    # 失败后继续执行
                    if issubclass(error_info[0], AssertionError):
                        self.test.recordFailStatus(error_info)
                    else:
                        self.test.recordErrorStatus(error_info)
                else:
                    raise e

    def _render_controller(self, step):
        self.template.init(step.collector.controller)
        step.collector.controller = self.template.render()

    def _render_content(self, step):
        self.template.init(step.collector.path)
        step.collector.path = self.template.render()
        if step.collector.others.get('params') is not None:
            query = step.collector.others.pop('params')
        else:
            query = None
        if step.collector.others.get('data') is not None:
            body = step.collector.others.pop('data')
            pop_key = 'data'
        elif step.collector.others.get('json') is not None:
            body = step.collector.others.pop('json')
            pop_key = 'json'
        else:
            body = None
            pop_key = None
        self.template.init(step.collector.others)
        step.collector.others = self.template.render()
        self.template.set_help_data(step.collector.path, step.collector.others.get('headers'), query, body)
        if query is not None:
            for expr, value in get_json_relation(query, "query"):
                if isinstance(value, str) and self.comp.search(value) is not None:
                    self.template.init(value)
                    render_value = self.template.render()
                    expression = self.json_path_parser.parse(expr)
                    expression.update(query, render_value)
                    self.template.request_query = query
            step.collector.others.setdefault("params", self.template.request_query)
        if body is not None:
            if step.collector.body_type in ("json", "form-urlencoded", "form-data"):
                for expr, value in get_json_relation(body, "body"):
                    if isinstance(value, str) and self.comp.search(value) is not None:
                        self.template.init(value)
                        render_value = self.template.render()
                        expression = self.json_path_parser.parse(expr)
                        expression.update(body, render_value)
                        self.template.request_body = body
            else:
                self.template.init(body)
                render_value = self.template.render()
                self.template.request_body = render_value
            step.collector.others.setdefault(pop_key, self.template.request_body)
        if step.collector.assertions is not None:
            self.template.init(step.collector.assertions)
            step.collector.assertions = self.template.render()
        if step.collector.relations is not None:
            self.template.init(step.collector.relations)
            step.collector.relations = self.template.render()
