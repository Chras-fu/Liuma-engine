from core.app.find_opt import *


class AppTestStep:
    def __init__(self, test, device, collector):
        self.test = test
        self.device = device
        self.collector = collector
        self.result = None

    def execute(self):
        try:
            self.test.debugLog('[{}]APP操作[{}]开始'.format(self.collector.id, self.collector.opt_name))
            opt_type = self.collector.opt_type
            if opt_type == "system":
                func = find_system_opt(self.collector.opt_name)
            elif opt_type == "view":
                func = find_view_opt(self.collector.opt_name)
            elif opt_type == "condition":
                func = find_condition_opt(self.collector.opt_name)
            elif opt_type == "assertion":
                func = find_assertion_opt(self.collector.opt_name)
            elif opt_type == "relation":
                func = find_relation_opt(self.collector.opt_name)
            else:
                func = find_scenario_opt(self.collector.opt_name)
            if func is None:
                raise NotExistedAppOperation("未定义操作")
            opt_content = {
                "system": self.collector.opt_system,
                "trans": self.collector.opt_trans,
                "code": self.collector.opt_code,
                "element": self.collector.opt_element,
                "data": self.collector.opt_data
            }
            self.result = func(self.test, self.device, **opt_content)
            self.log_show()
        finally:
            self.test.debugLog('[{}]APP操作[{}]结束'.format(self.collector.id, self.collector.opt_name))

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


class NotExistedAppOperation(Exception):
    """未定义的操作"""
