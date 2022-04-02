from core.web.find_opt import *


class UiTestStep:
    def __init__(self, test, driver, collector):
        self.test = test
        self.driver = driver
        self.collector = collector
        self.result = None

    def execute(self):
        try:
            self.test.debugLog('[{}]UI操作[{}]开始'.format(self.collector.id, self.collector.opt_name))
            opt_type = self.collector.opt_type
            if opt_type == "browser":
                func = find_browser_opt(self.collector.opt_name)
            elif opt_type == "page":
                func = find_page_opt(self.collector.opt_name)
            elif opt_type == "condition":
                func = find_condition_opt(self.collector.opt_name)
            elif opt_type == "assertion":
                func = find_assertion_opt(self.collector.opt_name)
            elif opt_type == "relation":
                func = find_relation_opt(self.collector.opt_name)
            else:
                func = find_scenario_opt(self.collector.opt_name)
            if func is None:
                raise NotExistedController("未定义控件")
            opt_content = {
                "trans": self.collector.opt_trans,
                "code": self.collector.opt_code,
                "element": self.collector.opt_element,
                "data": self.collector.opt_data
            }
            self.result = func(self.test, self.driver, **opt_content)
            self.log_show()
        finally:
            self.test.debugLog('[{}]UI操作[{}]结束'.format(self.collector.id, self.collector.opt_name))

    def log_show(self):
        msg = ""
        if self.collector.opt_element is not None:
            for k, v in self.collector.opt_element.items():
                msg += '元素定位: {}: {}<br>'.format(k, v)
        if self.collector.opt_data is not None:
            data_log = '{'
            for k, v in self.collector.opt_data.items():
                class_name = type(v).__name__
                data_log += "{}: {}, ".format(k, v)
            if len(data_log) > 1:
                data_log = data_log[:-2]
            data_log += '}'
            msg += '操作数据: {}'.format(data_log)
        if msg != "":
            msg = '操作信息: <br>' + msg
            self.test.debugLog(msg)


class NotExistedController(Exception):
    """未定义的控件"""
