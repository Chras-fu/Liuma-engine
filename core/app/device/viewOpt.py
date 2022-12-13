from uiautomator2 import UiObjectNotFoundError
from core.app.device import Operation


class View(Operation):
    """视图类操作"""

    def click(self):
        """点击"""
        try:
            self.test.debugLog("成功切换frame:%s")
        except UiObjectNotFoundError as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法切换frame:%s")
            raise e

    def custom(self, **kwargs):
        """自定义"""
        code = kwargs["code"]
        names = locals()
        names["element"] = kwargs["element"]
        names["data"] = kwargs["data"]
        names["device"] = self.device
        names["test"] = self.test
        try:
            exec(code)
            self.test.debugLog("成功执行 %s" % kwargs["trans"])
        except UiObjectNotFoundError as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
