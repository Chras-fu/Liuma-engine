from selenium.common.exceptions import NoSuchElementException


class Operation(object):
    def __init__(self, test, driver):
        self.driver = driver
        self.test = test

    def find_element(self, ele):
        """查找单个元素"""
        loc = (ele["by"].lower(), ele["expression"])
        try:
            element = self.driver.find_element(*tuple(loc))
            self.test.debugLog("成功定位元素 'By: %s Expression: %s'" % loc)
            return element
        except Exception as e:
            self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % loc)
            raise e

    def find_elements(self, ele):
        """查找批量元素"""
        loc = (ele["by"].lower(), ele["expression"])
        try:
            elements = self.driver.find_elements(*tuple(loc))
            if len(elements) > 0:
                self.test.debugLog("成功定位元素 'By: %s Expression: %s'" % loc)
                return elements
            else:
                self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % loc)
                raise NoSuchElementException("Failed to find elements 'By: %s Expression: %s'" % loc)
        except Exception as e:
            self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % loc)
            raise e

