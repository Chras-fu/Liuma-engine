from uiautomator2 import UiObjectNotFoundError
from core.assertion import LMAssert
from core.app.device import Operation


class Condition(Operation):
    """条件类操作"""

    def condition_ele_exists(self, element, assertion, expect):
        """判断元素存在"""
        try:
            actual = self.find_element(element).exists
            self.test.debugLog("成功获取元素exists:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素exists")
            raise e
        else:
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_ele_text(self, system, element, assertion, expect):
        """判断元素文本"""
        try:
            if system == "android":
                actual = self.find_element(element).get_text()
            else:
                actual = self.find_element(element).text()
            self.test.debugLog("成功获取元素text:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取元素text")
            raise e
        else:
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_ele_attribute(self, element, attribute, assertion, expect):
        """判断元素属性"""
        try:
            actual = self.find_element(element).info[attribute]
            self.test.debugLog("成功获取元素%s属性:%s" % (attribute, str(actual)))
        except Exception as e:
            self.test.errorLog("无法获取元素%s属性" % attribute)
            raise e
        else:
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_ele_center(self, system, element, assertion, expect):
        """判断元素位置"""
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
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_ele_x(self, system, element, assertion, expect):
        """判断元素X坐标"""
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
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_ele_y(self, system, element, assertion, expect):
        """判断元素Y坐标"""
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
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_alert_exists(self, assertion, expect):
        """判断弹框存在 IOS专属"""
        try:
            actual = self.device.alert.exists
            self.test.debugLog("成功获取弹框exists:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取弹框exists")
            raise e
        else:
            result, msg = LMAssert(assertion, actual, expect).compare()
            return result, msg

    def condition_alert_text(self, assertion, expect):
        """判断弹框文本 IOS专属"""
        try:
            actual = self.device.alert.text
            self.test.debugLog("成功获取弹框文本:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取弹框文本")
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
            """条件操作需要返回被判断的值 以sys_return(value)返回"""
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

