from uiautomator2 import UiObjectNotFoundError
from core.assertion import LMAssert
from core.app.device import Operation


class Condition(Operation):
    """条件类操作"""

    def condition_page_title(self, assertion, expect):
        """判断页面标题"""
        try:
            actual = self.device.title
            self.test.debugLog("成功获取title:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取title")
            raise e
        else:
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg
    
    def custom(self, **kwargs):
        """自定义"""
        code = kwargs["code"]
        names = locals()
        names["element"] = kwargs["element"]
        names["data"] = kwargs["data"]
        names["device"] = self.device
        names["test"] = self.test
        try:
            """条件操作需要返回被断言的值 以sys_return(value)返回"""
            def sys_return(res):
                names["_exec_result"] = res
            exec(code)
            self.test.debugLog("成功执行 %s" % kwargs["trans"])
        except UiObjectNotFoundError as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
        else:
            result, msg = LMAssert(kwargs["data"]["assertion"], names["_exec_result"], kwargs["data"]["expect"]).compare()
            return result, msg

