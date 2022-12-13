from selenium.common.exceptions import NoSuchElementException

from core.web.driver import Operation


class Relation(Operation):
    """关联类操作"""
    def get_page_title(self, save_name):
        """获取页面标题"""
        try:
            actual = self.driver.title
            self.test.debugLog("成功获取title:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取title")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_page_url(self, save_name):
        """获取页面url"""
        try:
            actual = self.driver.current_url
            self.test.debugLog("成功获取url:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取url")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_text(self, element, save_name):
        """获取元素文本"""
        try:
            actual = self.find_element(element).text
            self.test.debugLog("成功获取元素text:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素text")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_tag(self, element, save_name):
        """获取元素tag"""
        try:
            actual = self.find_element(element).tag_name
            self.test.debugLog("成功获取元素tag name:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素tag name")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_size(self, element, save_name):
        """获取元素尺寸"""
        try:
            actual = self.find_element(element).size
            self.test.debugLog("成功获取元素size:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素size")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_height(self, element, save_name):
        """获取元素高度"""
        try:
            actual = self.find_element(element).size.get("height")
            self.test.debugLog("成功获取元素height:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素height")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_width(self, element, save_name):
        """获取元素宽度"""
        try:
            actual = self.find_element(element).size.get("width")
            self.test.debugLog("成功获取元素width:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素width")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_location(self, element, save_name):
        """获取元素位置"""
        try:
            actual = self.find_element(element).location
            self.test.debugLog("成功获取元素location:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素location")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_x(self, element, save_name):
        """获取元素X坐标"""
        try:
            actual = self.find_element(element).location.get("x")
            self.test.debugLog("成功获取元素location x:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素location x")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_y(self, element, save_name):
        """获取元素Y坐标"""
        try:
            actual = self.find_element(element).location.get("y")
            self.test.debugLog("成功获取元素location y:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素location y")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_attribute(self, element, name, save_name):
        """获取元素属性"""
        try:
            actual = self.find_element(element).get_attribute(name)
            self.test.debugLog("成功获取元素attribute:%s" % str(actual))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素attribute")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_ele_css(self, element, name, save_name):
        """获取元素css样式"""
        try:
            actual = self.find_element(element).value_of_css_property(name)
            self.test.debugLog("成功获取元素css %s:%s" % (name, str(actual)))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法获取元素css %s" % name)
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_position(self, save_name):
        """获取窗口位置"""
        try:
            actual = self.driver.get_window_position()
            self.test.debugLog("成功获取窗口position:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口position")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_x(self, save_name):
        """获取窗口X坐标"""
        try:
            actual = self.driver.get_window_position().get("x")
            self.test.debugLog("成功获取窗口position x:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口position x")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_y(self, save_name):
        """获取窗口Y坐标"""
        try:
            actual = self.driver.get_window_position().get("y")
            self.test.debugLog("成功获取窗口position y:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口position y")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_size(self, save_name):
        """获取窗口大小"""
        try:
            actual = self.driver.get_window_size()
            self.test.debugLog("成功获取窗口size:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口size")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_width(self, save_name):
        """获取窗口宽度"""
        try:
            actual = self.driver.get_window_size().get("width")
            self.test.debugLog("成功获取窗口width:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口width")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_window_height(self, save_name):
        """获取窗口高度"""
        try:
            actual = self.driver.get_window_size().get("height")
            self.test.debugLog("成功获取窗口height:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取窗口height")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_current_handle(self, save_name):
        """获取当前窗口句柄"""
        try:
            actual = self.driver.current_window_handle
            self.test.debugLog("成功获取当前窗口handle:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取当前窗口handle")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_all_handle(self, save_name):
        """获取所有窗口句柄"""
        try:
            actual = self.driver.window_handles
            self.test.debugLog("成功获取所有窗口handle:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取所有窗口handle")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_cookies(self, save_name):
        """获取cookies"""
        try:
            actual = self.driver.get_cookies()
            self.test.debugLog("成功获取cookies:%s" % str(actual))
        except Exception as e:
            self.test.errorLog("无法获取cookies")
            raise e
        else:
            self.test.context[save_name] = actual

    def get_cookie(self, name, save_name):
        """获取cookie"""
        try:
            actual = self.driver.get_cookie(name)
            self.test.debugLog("成功获取cookie %s:%s" % (name, str(actual)))
        except Exception as e:
            self.test.errorLog("无法获取cookie:%s" % name)
            raise e
        else:
            self.test.context[save_name] = actual

    def custom(self, **kwargs):
        """自定义"""
        code = kwargs["code"]
        names = locals()
        names["element"] = kwargs["element"]
        names["data"] = kwargs["data"]
        names["driver"] = self.driver
        names["test"] = self.test
        try:
            """关联操作需要返回被断言的值 以sys_return(value)返回"""
            def sys_return(res):
                names["_exec_result"] = res
            exec(code)
            self.test.debugLog("成功执行 %s" % kwargs["trans"])
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
        else:
            self.test.context[kwargs["data"]["save_name"]] = names["_exec_result"]

