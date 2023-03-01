import sys
from jsonpath_ng.parser import JsonPathParser
from core.template import Template
from core.app.collector import WebOperationCollector
from core.app.teststep import AppTestStep
from core.app.device import connect_device
from tools.utils.utils import get_case_message, handle_operation_data, handle_params_data
import re


class AppTestCase:
    def __init__(self, test):
        self.test = test
        self.context = test.context
        self.case_message = get_case_message(test.test_data)
        self.id = self.case_message['caseId']
        self.name = self.case_message['caseName']
        setattr(test, 'test_case_name', self.case_message['caseName'])
        setattr(test, 'test_case_desc', self.case_message['comment'])
        self.functions = self.case_message['functions']
        self.params = handle_params_data(self.case_message['params'])
        self.device = self._before_execute()
        self.template = Template(self.context, self.functions, self.params)
        self.parser = JsonPathParser()
        self.comp = re.compile(r"\{\{.*?\}\}")
        self.skip_opts = list()

    def execute(self):
        opt_content = None
        if self.case_message['optList'] is None:
            self._after_execute()
            raise RuntimeError("无法获取APP测试相关数据, 请重试!!!")
        step_count = len(self.case_message['optList'])
        step_n = 0
        try:
            while step_n < step_count:
                if step_n in self.skip_opts:
                    step_n += 1
                    continue
                opt_content = self.case_message['optList'][step_n]
                self.test.defineTrans(opt_content["operationId"], opt_content['operationTrans'],
                                      self._get_opt_content(opt_content['operationElement']), opt_content['operationDesc'])
                collector = WebOperationCollector()
                collector.collect(opt_content)
                step = AppTestStep(self.test, self.device, collector)
                self._render(step)
                step.execute()
                self._assert_solve(step)
                self._condition_solve(step, step_n)
                step_n += 1
        except Exception as e:
            if not isinstance(e, AssertionError):
                self.test.saveScreenShot(opt_content['operationTrans'] if opt_content is not None else opt_content,
                                         self.device.screenshot(format='raw'))
            raise e
        finally:
            self._after_execute()

    @staticmethod
    def _get_opt_content(elements):
        content = ""
        if elements is not None:
            for key, element in elements.items():
                content = "%s\n %s: %s" % (content, key, element["target"])
        return content

    def _before_execute(self):
        if self.case_message['deviceUrl'] is None:
            raise Exception("执行设备不在线 本用例执行失败")
        device = connect_device(self.case_message['deviceSystem'], f"http://{self.case_message['deviceUrl']}")
        if self.case_message['deviceSystem'] == 'android':
            device.app_start(self.case_message['appId'], self.case_message['activity'])
            return device
        else:
            device = device.session(self.case_message['appId'])
            return device

    def _after_execute(self):
        self.device.app_stop(self.case_message['appId'])

    def _render(self, step):
        if step.collector.opt_data is not None:
            for expr, param in step.collector.opt_data.items():
                param_value = param["value"]
                if isinstance(param_value, str) and self.comp.search(param_value) is not None:
                    self.template.init(param_value)
                    render_value = self.template.render()
                    param["value"] = render_value
            step.collector.opt_data = handle_operation_data(step.collector.opt_data)

    def _assert_solve(self, step):
        if step.collector.opt_type == "assertion":
            if step.result[0]:
                self.test.debugLog('[{}][{}]断言成功: {}'.format(step.collector.id,
                                                             step.collector.opt_name,
                                                             step.result[1]))
            else:
                self.test.errorLog('[{}][{}]断言失败: {}'.format(step.collector.id,
                                                             step.collector.opt_name,
                                                             step.result[1]))
                self.test.saveScreenShot(step.collector.opt_trans, self.device.screenshot())
                if "continue" in step.collector.opt_data and step.collector.opt_data["continue"] is True:
                    try:
                        raise AssertionError(step.result[1])
                    except AssertionError:
                        error_info = sys.exc_info()
                        self.test.recordFailStatus(error_info)
                else:
                    raise AssertionError(step.result[1])

    def _condition_solve(self, step, current):
        if step.collector.opt_type == "condition":
            offset_true = step.collector.opt_data["true"]
            if not isinstance(offset_true, int):
                offset_true = 0
            offset_false = step.collector.opt_data["false"]
            if not isinstance(offset_false, int):
                offset_false = 0
            if step.result[0]:
                self.test.debugLog('[{}][{}]判断成功, 执行成功分支: {}'.format(step.collector.id,
                                                                     step.collector.opt_name,
                                                                     step.result[1]))
                self.skip_opts.extend([current + i for i in range(offset_true + 1, offset_true + offset_false + 1)])
            else:
                self.test.errorLog('[{}][{}]判断失败, 执行失败分支: {}'.format(step.collector.id,
                                                                     step.collector.opt_name,
                                                                     step.result[1]))
                self.skip_opts.extend([current + i for i in range(1, offset_true + 1)])
