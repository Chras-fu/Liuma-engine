from uiautomator2 import UiObjectNotFoundError
from core.app.device import Operation


class Relation(Operation):
    """关联类操作"""
    def get_page_title(self, save_name):
        """获取页面标题"""
        try:
            actual = self.device.title
            self.test.debugLog("成功获取title:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取title")
            raise e
        else:
            self.test.context[save_name] = actual

    def custom(self, **kwargs):
        """自定义"""
        code = kwargs["code"]
        names = locals()
        names["element"] = kwargs["element"]
        names["data"] = kwargs["data"]
        names["device"] = self.device
        names["test"] = self.test
        try:
            """关联操作需要返回被断言的值 以sys_return(value)返回"""
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
            self.test.context[kwargs["data"]["save_name"]] = names["_exec_result"]

