from core.template import Template
from core.app.collector import AppOperationCollector
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
        test.common_params = self.params
        self.device = self.before_execute()
        self.template = Template(self.test, self.context, self.functions, self.params)
        self.comp = re.compile(r"\{\{.*?\}\}")

    def execute(self):
        if self.case_message['optList'] is None:
            self.after_execute()
            raise RuntimeError("无法获取APP测试相关数据, 请重试!!!")
        try:
            self.loop_execute(self.case_message['optList'], [])
        finally:
            self.after_execute()

    def loop_execute(self, opt_list, skip_opts, step_n=0):
        while step_n < len(opt_list):
            opt_content = opt_list[step_n]
            # 定义收集器
            collector = AppOperationCollector()
            step = AppTestStep(self.test, self.device, self.context, collector)
            # 定义事务
            self.test.defineTrans(opt_content["operationId"], opt_content['operationTrans'],
                                  self.get_opt_content(opt_content['operationElement']), opt_content['operationDesc'])
            if step_n in skip_opts:
                self.test.updateTransStatus(3)
                self.test.debugLog('[{}]操作在条件控制之外不被执行'.format(opt_content['operationTrans']))
                step_n += 1
                continue
            # 收集步骤信息
            step.collector.collect(opt_content)
            try:
                if step.collector.opt_type == "looper":
                    looper_step_num = step.looper_controller(self, opt_list, step_n)
                    step_n += looper_step_num + 1
                else:
                    # 渲染主体
                    self.render_content(step)
                    step.execute()
                    step.assert_controller()
                    skip_opts.extend(step.condition_controller(step_n))
                    step_n += 1
            except Exception as e:
                if not isinstance(e, AssertionError):
                    self.test.saveScreenShot(opt_content['operationTrans'], self.device.screenshot(format='raw'))
                raise e

    @staticmethod
    def get_opt_content(elements):
        content = ""
        if elements is not None:
            for key, element in elements.items():
                content = "%s\n %s: %s" % (content, key, element["target"])
        return content

    def before_execute(self):
        if self.case_message['deviceUrl'] is None:
            raise Exception("执行设备不在线 本用例执行失败")
        device = connect_device(self.case_message['deviceSystem'], f"http://{self.case_message['deviceUrl']}")
        if self.case_message['deviceSystem'] == 'android':
            device.app_start(self.case_message['appId'], self.case_message['activity'])
            return device
        else:
            device = device.session(self.case_message['appId'])
            return device

    def after_execute(self):
        self.device.app_stop(self.case_message['appId'])

    def render_looper(self, looper):
        self.template.init(looper)
        _looper = self.template.render()
        for name, param in _looper.items():
            if name != "target" or name != "expect":    # 断言实际值不作数据处理
                _looper[name] = handle_operation_data(param["type"], param["value"])
        if "times" in _looper:
            try:
                times = int(_looper["times"])
            except:
                times = 1
            _looper["times"] = times
        return _looper

    def render_content(self, step):
        if step.collector.opt_element is not None:
            for name, expression in step.collector.opt_element.items():
                if self.comp.search(str(expression)) is not None:
                    self.template.init(expression)
                    expression = self.template.render()
                step.collector.opt_element[name] = expression
        if step.collector.opt_data is not None:
            data = {}
            for name, param in step.collector.opt_data.items():
                param_value = param["value"]
                if isinstance(param_value, str) and self.comp.search(param_value) is not None:
                    self.template.init(param_value)
                    param_value = self.template.render()
                data[name] = handle_operation_data(param["type"], param_value)
            step.collector.opt_data = data

