from time import sleep

from uiautomator2 import UiObjectNotFoundError
from wda import WDAElementNotFoundError
from core.app.device import Operation


class System(Operation):
    """系统操作"""

    def start_app(self, app_id):
        """启动应用"""
        try:
            self.device.app_start(app_id)
            self.test.debugLog("成功执行启动应用")
        except Exception as e:
            self.test.errorLog("无法执行关闭应用")
            raise e

    def close_app(self, app_id):
        """关闭应用"""
        try:
            self.device.app_stop(app_id)
            self.test.debugLog("成功执行关闭应用")
        except Exception as e:
            self.test.errorLog("无法执行关闭应用")
            raise e

    def swipe_left(self, system):
        """左滑"""
        try:
            if system == "android":
                self.device.swipe_ext("left")
            else:
                self.device.swipe_left()
            self.test.debugLog("成功执行左滑")
        except Exception as e:
            self.test.errorLog("无法执行左滑")
            raise e

    def swipe_right(self, system):
        """右滑"""
        try:
            if system == "android":
                self.device.swipe_ext("right")
            else:
                self.device.swipe_right()
            self.test.debugLog("成功执行右滑")
        except Exception as e:
            self.test.errorLog("无法执行右滑")
            raise e

    def swipe_up(self, system):
        """上滑"""
        try:
            if system == "android":
                self.device.swipe_ext("up")
            else:
                self.device.swipe_up()
            self.test.debugLog("成功执行上滑")
        except Exception as e:
            self.test.errorLog("无法执行上滑")
            raise e

    def swipe_down(self, system):
        """下滑"""
        try:
            if system == "android":
                self.device.swipe_ext("down")
            else:
                self.device.swipe_down()
            self.test.debugLog("成功执行下滑")
        except Exception as e:
            self.test.errorLog("无法执行下滑")
            raise e

    def home(self, system):
        """系统首页"""
        try:
            if system == "android":
                self.device.keyevent("home")
            else:
                self.device.home()
            self.test.debugLog("成功执行返回系统首页")
        except Exception as e:
            self.test.errorLog("无法执行返回系统首页")
            raise e

    def back(self):
        """系统返回 安卓专用"""
        try:
            self.device.keyevent("back")
            self.test.debugLog("成功执行返回")
        except Exception as e:
            self.test.errorLog("无法执行返回")
            raise e

    def press(self, keycode):
        """系统按键"""
        try:
            self.device.press(keycode)
            self.test.debugLog("成功执行按下系统键位: %s" % keycode)
        except Exception as e:
            self.test.errorLog("无法执行按下系统键位: %s" % keycode)
            raise e

    def screenshot(self, name):
        """屏幕截图"""
        try:
            screenshot = self.device.screenshot()
            self.test.saveScreenShot(name, screenshot)
            self.test.debugLog("成功执行屏幕截图")
        except Exception as e:
            self.test.errorLog("无法执行屏幕截图")
            raise e

    def screen_on(self, system):
        """亮屏"""
        try:
            if system == "android":
                self.device.screen_on()
            else:
                self.device.unlock()
            self.test.debugLog("成功执行亮屏")
        except Exception as e:
            self.test.errorLog("无法执行亮屏")
            raise e

    def screen_off(self, system):
        """息屏"""
        try:
            if system == "android":
                self.device.screen_off()
            else:
                self.device.lock()
            self.test.debugLog("成功执行息屏")
        except Exception as e:
            self.test.errorLog("无法执行息屏")
            raise e

    def sleep(self, second):
        """强制等待"""
        try:
            sleep(second)
            self.test.debugLog("成功执行sleep %ds" % second)
        except Exception as e:
            self.test.errorLog("无法执行sleep %ds" % second)
            raise e

    def implicitly_wait(self, second):
        """隐式等待"""
        try:
            self.device.implicitly_wait(second)
            self.test.debugLog("成功执行implicitly wait %ds" % second)
        except Exception as e:
            self.test.errorLog("无法执行implicitly wait %ds" % second)
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
