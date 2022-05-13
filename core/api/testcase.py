import re

from core.api.collection import ApiRequestCollector
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
        if self.case_message['apiList'] is None:
            raise RuntimeError("无法获取API相关数据, 请重试!!!")
        for api_data in self.case_message['apiList']:
            self.test.defineTrans(api_data['apiId'], api_data['apiName'], api_data['path'])
            collector = ApiRequestCollector()
            collector.collect(api_data)
            step = ApiTestStep(self.test, self.session, collector, self.context)
            self._render(step)
            step.execute()
            if step.assert_result['result']:
                self.test.debugLog('[{}][{}]接口断言成功: {}'.format(step.collector.apiId,
                                                               step.collector.apiName,
                                                               log_msg(step.assert_result['checkMessages'])))
            else:
                self.test.errorLog('[{}][{}]接口断言失败: {}'.format(step.collector.apiId,
                                                               step.collector.apiName,
                                                               log_msg(step.assert_result['checkMessages'])))
                raise AssertionError(log_msg(step.assert_result['checkMessages']))

    def _render(self, step):
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
