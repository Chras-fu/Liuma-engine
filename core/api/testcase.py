import re
import sys

from core.api.collector import ApiRequestCollector
from core.template import Template
from core.api.teststep import ApiTestStep, dict2str
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
        self.template = Template(self.test, self.context, self.functions, self.params)
        self.json_path_parser = JsonPathParser()
        self.comp = re.compile(r"\{\{.*?\}\}")

    def execute(self):
        """用例执行入口函数"""
        if self.case_message['apiList'] is None:
            raise RuntimeError("无法获取API相关数据, 请重试!!!")
        self.loop_execute(self.case_message['apiList'], "root")

    def loop_execute(self, api_list, loop_id, step_n=0):
        """循环执行"""
        while step_n < len(api_list):
            api_data = api_list[step_n]
            # 定义收集器
            collector = ApiRequestCollector()
            step = ApiTestStep(self.test, self.session, collector, self.context, self.params)
            # 循环控制器
            step.collector.collect_looper(api_data)
            if len(step.collector.looper) > 0 and not (loop_id != "root" and step_n == 0):
                # 非根循环 且并非循环第一个接口时才执行循环 从而避免循环套循环情况下的死循环
                step.looper_controller(self, api_list, step_n)
                step_n = step_n + step.collector.looper["num"] - 1  # 跳过本次循环中执行的接口
                continue  # 母循环最后一个接口索引必须超过子循环的最后一个接口索引 否则超过母循环的接口无法执行
            step_n += 1
            # 定义事务
            self.test.defineTrans(api_data['apiId'], api_data['apiName'], api_data['path'], api_data['apiDesc'])
            # 条件控制器
            step.collector.collect_conditions(api_data)
            if len(step.collector.conditions) > 0:
                result = step.condition_controller(self)
                if result is not True:
                    self.test.updateTransStatus(3)  # 任意条件不满足 跳过执行
                    self.test.debugLog('[{}]接口条件控制器判断为否: {}'.format(api_data['apiName'], result))
                    continue
            # 收集请求主体并执行
            step.collector.collect(api_data)
            try:
                # 执行前置脚本和sql
                if step.collector.controller["pre"] is not None:
                    for pre in step.collector.controller["pre"]:
                        if pre['name'] == 'preScript':
                            step.exec_script(pre["value"])
                        else:
                            step.exec_sql(pre["value"], self)
                # 渲染主体
                self.render_content(step)
                # 执行step, 接口参数移除，接口请求，接口响应，断言操作，依赖参数提取
                step.execute()
                # 执行后置脚本和sql
                if step.collector.controller["post"] is not None:
                    for post in step.collector.controller["post"]:
                        if post['name'] == 'postScript':
                            step.exec_script(post["value"])
                        else:
                            step.exec_sql(post["value"], self)
                # 检查step的断言结果
                if step.assert_result['result']:
                    self.test.debugLog('[{}]接口断言成功: {}'.format(step.collector.apiName,
                                                                   dict2str(step.assert_result['checkMessages'])))
                else:
                    self.test.errorLog('[{}]接口断言失败: {}'.format(step.collector.apiName,
                                                                   dict2str(step.assert_result['checkMessages'])))
                    raise AssertionError(dict2str(step.assert_result['checkMessages']))
            except Exception as e:
                error_info = sys.exc_info()
                if collector.controller["errorContinue"].lower() == "true":
                    # 失败后继续执行
                    if issubclass(error_info[0], AssertionError):
                        self.test.recordFailStatus(error_info)
                    else:
                        self.test.recordErrorStatus(error_info)
                else:
                    raise e

    def render_looper(self, looper):
        self.template.init(looper)
        _looper = self.template.render()
        if "times" in _looper:
            try:
                times = int(_looper["times"])
            except:
                times = 1
            _looper["times"] = times
        return _looper

    def render_conditions(self, conditions):
        self.template.init(conditions)
        return self.template.render()

    def render_sql(self, sql):
        self.template.init(sql)
        return self.template.render()

    def render_content(self, step):
        self.template.init(step.collector.path)
        step.collector.path = self.template.render()
        if step.collector.others.get('headers') is not None:
            headers = step.collector.others.pop('headers')
        else:
            headers = None
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
        self.template.set_help_data(step.collector.path, headers, query, body)
        if "#{_REQUEST_QUERY}" in str(headers) or "#{_REQUEST_BODY}" in str(headers):
            self.render_json(step, query, "query")
            self.render_json(step, body, "body", pop_key)
            self.render_json(step, headers, "headers")
        else:
            self.render_json(step, headers, "headers")
            self.render_json(step, query, "query")
            self.render_json(step, body, "body", pop_key)
        if step.collector.assertions is not None:
            self.template.init(step.collector.assertions)
            step.collector.assertions = self.template.render()
        if step.collector.relations is not None:
            self.template.init(step.collector.relations)
            step.collector.relations = self.template.render()

    def render_json(self, step, data, name, pop_key=None):
        if data is None:
            return
        if name == "body" and step.collector.body_type not in ("json", "form-urlencoded", "form-data"):
            self.template.init(data)
            render_value = self.template.render()
            self.template.request_body = render_value
        else:
            for expr, value in get_json_relation(data, "body"):
                if isinstance(value, str) and self.comp.search(value) is not None:
                    self.template.init(value)
                    render_value = self.template.render()
                    if name == "headers":
                        render_value = str(render_value)
                    expression = self.json_path_parser.parse(expr)
                    expression.update(data, render_value)
                    if name == "body":
                        self.template.request_body = data
                    elif name == "query":
                        self.template.request_query = data
                    else:
                        self.template.request_headers = data
        if name == "body":
            step.collector.others.setdefault(pop_key, self.template.request_body)
        elif name == "query":
            step.collector.others.setdefault("params", self.template.request_query)
        else:
            step.collector.others.setdefault("headers", self.template.request_headers)

