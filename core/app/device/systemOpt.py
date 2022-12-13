from uiautomator2 import UiObjectNotFoundError
from wda import WDAElementNotFoundError
from core.app.device import Operation


class System(Operation):
    """系统操作"""

    def swipe(self, system, ):
        """坐标滑动"""

    def swipe_left(self, system, app_id, activity=None):
        """启动应用"""
        try:
            if system == "android":
                if activity == "":
                    activity = None
                self.device.app_start(app_id, activity)
            else:
                self.device.app_launch(app_id)
            self.test.debugLog("成功执行启动应用")
        except Exception as e:
            self.test.errorLog("无法执行启动应用")
            raise e

    def close_app(self, system, app_id):
        """关闭应用"""
        try:
            if system == "android":
                self.device.app_stop(app_id)
            else:
                self.device.app_terminate(app_id)
            self.test.debugLog("成功执行关闭应用")
        except Exception as e:
            self.test.errorLog("无法执行关闭应用")
            raise e

    def swipe_screen(self, system, app_id):
        """滑动屏幕"""
        try:
            if system == "android":
                self.device.app_stop(app_id)
            else:
                self.device.app_terminate(app_id)
            self.test.debugLog("成功执行关闭应用")
        except Exception as e:
            self.test.errorLog("无法执行关闭应用")
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
        except WDAElementNotFoundError as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
