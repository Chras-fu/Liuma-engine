from uiautomator2 import UiObjectNotFoundError
from core.app.device import Operation


class Relation(Operation):
    """关联类操作"""
    def get_window_size(self, system, save_name):
        """获取屏幕尺寸"""
        try:
            if system == "android":
                w, h = self.device.window_size()
                actual = (w, h)
            else:
                size = self.device.window_size()
                actual = (size.width, size.height)
            self.test.debugLog("成功获取屏幕尺寸:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取屏幕尺寸")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_width(self, system, save_name):
        """获取屏幕宽度"""
        try:
            if system == "android":
                w, h = self.device.window_size()
                actual = w
            else:
                size = self.device.window_size()
                actual = size.width
            self.test.debugLog("成功获取屏幕宽度:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取屏幕宽度")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_height(self, system, save_name):
        """获取屏幕高度"""
        try:
            if system == "android":
                w, h = self.device.window_size()
                actual = h
            else:
                size = self.device.window_size()
                actual = size.height
            self.test.debugLog("成功获取屏幕高度:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取屏幕高度")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_text(self, system, element, save_name):
        """获取元素文本"""
        try:
            if system == "android":
                actual = self.find_element(element).get_text()
            else:
                actual = self.find_element(element).text()
            self.test.debugLog("成功获取元素文本:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素文本")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_center(self, system, element, save_name):
        """获取元素位置"""
        try:
            if system == "android":
                x, y = self.find_element(element).center()
                actual = (x, y)
            else:
                size = self.find_element(element).bounds.center()
                actual = (size.x, size.y)
            self.test.debugLog("成功获取元素位置:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素位置")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_x(self, system, element, save_name):
        """获取元素X坐标"""
        try:
            if system == "android":
                x, y = self.find_element(element).center()
                actual = x
            else:
                size = self.find_element(element).bounds.center()
                actual = size.x
            self.test.debugLog("成功获取元素X坐标:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素X坐标")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_y(self, system, element, save_name):
        """获取元素Y坐标"""
        try:
            if system == "android":
                x, y = self.find_element(element).center()
                actual = y
            else:
                size = self.find_element(element).bounds.center()
                actual = size.y
            self.test.debugLog("成功获取元素Y坐标:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素Y坐标")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_alert_text(self, save_name):
        """获取弹框文本 IOS专属"""
        try:
            actual = self.device.alert.text
            self.test.debugLog("成功获取弹框文本:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取弹框文本")
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
            """关联操作需要返回被关联的值 以sys_return(value)返回"""
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

