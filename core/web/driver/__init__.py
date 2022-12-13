from selenium.common.exceptions import NoSuchElementException


class Operation(object):
    def __init__(self, test, driver):
        self.driver = driver
        self.test = test

    def find_element(self, ele):
        """查找单个元素"""
        try:
            element = self.driver.find_element(*tuple(ele))
            self.test.debugLog("成功定位元素 'By: %s Expression: %s'" % ele)
            return element
        except Exception as e:
            self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % ele)
            raise e

    def find_elements(self, ele):
        """查找批量元素"""
        try:
            elements = self.driver.find_elements(*tuple(ele))
            if len(elements) > 0:
                self.test.debugLog("成功定位元素 'By: %s Expression: %s'" % ele)
                return elements
            else:
                self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % ele)
                raise NoSuchElementException("Failed to find elements 'By: %s Expression: %s'" % ele)
        except Exception as e:
            self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % ele)
            raise e

