import re
from selenium import webdriver
from core.template import Template
from core.web.collector import WebOperationCollector
from core.web.teststep import WebTestStep
from tools.utils.utils import get_case_message, handle_operation_data, handle_params_data


class WebTestCase:
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
        self.template = Template(self.context, self.functions, self.params)
        self.driver = self.before_execute()
        self.comp = re.compile(r"\{\{.*?\}\}")

    def execute(self):
        if self.case_message['optList'] is None:
            self.after_execute()
            raise RuntimeError("无法获取WEB测试相关数据, 请重试!!!")
        try:
            self.loop_execute(self.case_message['optList'], [])
        finally:
            self.after_execute()

    def loop_execute(self, opt_list, skip_opts, step_n=0):
        while step_n < len(opt_list):
            opt_content = opt_list[step_n]
            # 定义收集器
            collector = WebOperationCollector()
            step = WebTestStep(self.test, self.driver, self.context, collector)
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
                    self.test.saveScreenShot(opt_content['operationTrans'], self.driver.get_screenshot_as_png())
                raise e

    @staticmethod
    def get_opt_content(elements):
        content = ""
        if elements is not None:
            for key, element in elements.items():
                content = "%s\n %s: %s" % (content, key, element["target"])
        return content

    def before_execute(self):
        old_driver = self.test.driver.driver
        if self.case_message["startDriver"]:
            # 读取配置
            opt = webdriver.ChromeOptions()
            driver_setting = self.render_driver(self.case_message["driverSetting"])
            if "arguments" in driver_setting.keys():
                for item in driver_setting["arguments"]:
                    if item["value"] != "":
                        opt.add_argument(item["value"])
            if "experimentals" in driver_setting.keys():
                for item in driver_setting["experimentals"]:
                    if item["name"] != "" and item["value"] != "":
                        opt.add_experimental_option(item["name"], handle_operation_data(item))
            if "extensions" in driver_setting.keys():
                for item in driver_setting["extensions"]:
                    if item["value"] != "":
                        opt.add_encoded_extension(item["value"])
            if "files" in driver_setting.keys():
                for item in driver_setting["files"]:
                    if item["value"] != "":
                        opt.add_extension(item["value"])
            if "binary" in driver_setting.keys() and driver_setting["binary"] != "":
                opt.binary_location = driver_setting["binary"]
            if self.test.driver.browser_opt == "headless":
                opt.add_argument("--headless")
                opt.add_argument("--no-sandbox")
            elif self.test.driver.browser_opt == "remote":
                caps = {
                    'browserName': 'chrome'
                }
            else:
                opt.add_experimental_option('excludeSwitches', ['enable-logging'])
            if old_driver is not None:
                old_driver.quit()
            self.test.driver.driver = None
            if self.test.driver.browser_opt == "remote":
                return webdriver.Remote(command_executor=self.test.driver.browser_path,
                                        desired_capabilities=caps, options=opt)
            else:
                return webdriver.Chrome(executable_path=self.test.driver.browser_path, options=opt)
        else:
            if old_driver is not None:
                return old_driver
            else:
                raise RuntimeError("无法找到已启动的浏览器进程 请检查用例开关驱动配置")

    def after_execute(self):
        if self.case_message["closeDriver"]:
            self.driver.quit()
            self.test.driver.driver = None
        else:
            self.test.driver.driver = self.driver

    def render_driver(self, driver_setting):
        self.template.init(driver_setting)
        return self.template.render()

    def render_looper(self, looper):
        self.template.init(looper)
        _looper = self.template.render()
        for name, param in _looper.items():
            if name != "target" or name != "expect":    # 断言实际值不作数据处理
                _looper[name] = handle_operation_data(param)
        if "times" in _looper:
            try:
                times = int(_looper["times"])
            except:
                times = 1
            _looper["times"] = times
        return _looper

    def render_content(self, step):
        if step.collector.opt_element is not None:
            for name, expressions in step.collector.opt_element.items():
                expression = expressions[1]
                if self.comp.search(str(expression)) is not None:
                    self.template.init(expression)
                    render_value = self.template.render()
                    expressions = (expressions[0], str(render_value))
                step.collector.opt_element[name] = expressions
        if step.collector.opt_data is not None:
            data = {}
            for name, param in step.collector.opt_data.items():
                param_value = param["value"]
                if isinstance(param_value, str) and self.comp.search(param_value) is not None:
                    self.template.init(param_value)
                    render_value = self.template.render()
                    param["value"] = render_value
                data[name] = handle_operation_data(param)
            step.collector.opt_data = data

