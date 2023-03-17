import datetime
import sys
from core.assertion import LMAssert
from core.web.find_opt import *


class WebTestStep:
    def __init__(self, test, driver, context, collector):
        self.test = test
        self.driver = driver
        self.context = context
        self.collector = collector
        self.result = None

    def execute(self):
        try:
            self.test.debugLog('WEB操作[{}]开始'.format(self.collector.opt_name))
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
                raise NotExistedWebOperation("未定义操作")
            opt_content = {
                "trans": self.collector.opt_trans,
                "code": self.collector.opt_code,
                "element": self.collector.opt_element,
                "data": self.collector.opt_data
            }
            self.result = func(self.test, self.driver, **opt_content)
            self.log_show()
        finally:
            self.test.debugLog('WEB操作[{}]结束'.format(self.collector.opt_name))

    def looper_controller(self, case, opt_list, step_n):
        """循环控制器"""
        if self.collector.opt_trans == "While循环":
            loop_start_time = datetime.datetime.now()
            timeout = int(self.collector.opt_data["timeout"]["value"])
            while timeout == 0 or (datetime.datetime.now() - loop_start_time).seconds * 1000 < timeout:
                # timeout为0时可能会死循环 慎重选择
                _looper = case.render_looper(self.collector.opt_data) # 渲染循环控制控制器 每次循环都需要渲染
                result, _ = LMAssert(_looper['assertion'], _looper['target'], _looper['expect']).compare()
                if not result:
                    return _looper["num"]
                _opt_list = opt_list[step_n+1: (step_n + _looper["num"])]   # 循环操作本身不参与循环 不然死循环
                case.loop_execute(_opt_list, [])
        else:
            _looper = case.render_looper(self.collector.looper) # 渲染循环控制控制器 for只需渲染一次
            for index in range(_looper["times"]):  # 本次循环次数
                self.context[_looper["indexName"]] = index  # 给循环索引赋值第几次循环 母循环和子循环的索引名不应一样
                _opt_list = opt_list[step_n+1: (step_n + _looper["num"])]
                case.loop_execute(_opt_list, [])

    def assert_controller(self):
        if self.collector.opt_type == "assertion":
            if self.result[0]:
                self.test.debugLog('[{}]断言成功: {}'.format(self.collector.opt_trans,
                                                             self.result[1]))
            else:
                self.test.errorLog('[{}]断言失败: {}'.format(self.collector.opt_trans,
                                                             self.result[1]))
                self.test.saveScreenShot(self.collector.opt_trans, self.driver.get_screenshot_as_png())
                if "continue" in self.collector.opt_data and self.collector.opt_data["continue"] is True:
                    try:
                        raise AssertionError(self.result[1])
                    except AssertionError:
                        error_info = sys.exc_info()
                        self.test.recordFailStatus(error_info)
                else:
                    raise AssertionError(self.result[1])

    def condition_controller(self, current):
        if self.collector.opt_type == "condition":
            offset_true = self.collector.opt_data["true"]
            if not isinstance(offset_true, int):
                offset_true = 0
            offset_false = self.collector.opt_data["false"]
            if not isinstance(offset_false, int):
                offset_false = 0
            if self.result[0]:
                self.test.debugLog('[{}]判断成功, 执行成功分支: {}'.format(self.collector.opt_name,
                                                                        self.result[1]))
                return [current + i for i in range(offset_true + 1, offset_true + offset_false + 1)]
            else:
                self.test.errorLog('[{}]判断失败, 执行失败分支: {}'.format(self.collector.opt_name,
                                                                        self.result[1]))
                return [current + i for i in range(1, offset_true + 1)]
        return []

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


class NotExistedWebOperation(Exception):
    """未定义的WEB操作"""
