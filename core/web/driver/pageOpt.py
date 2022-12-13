from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from core.web.driver import Operation


class Page(Operation):
    """网页类操作"""

    def switch_frame(self, frame):
        """切换框架"""
        try:
            frame_reference = self.find_element(frame)
            self.driver.switch_to.frame(frame_reference)
            self.test.debugLog("成功切换frame:%s" % frame[1])
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法切换frame:%s" % frame[1])
            raise e

    def switch_content(self):
        """返回默认框架"""
        try:
            self.driver.switch_to.default_content()
            self.test.debugLog("成功切换default content")
        except Exception as e:
            self.test.errorLog("无法切换default content")
            raise e

    def switch_parent(self):
        """返回父框架"""
        try:
            self.driver.switch_to.parent_frame()
            self.test.debugLog("成功切换parent content")
        except Exception as e:
            self.test.errorLog("无法切换parent content")
            raise e

    def alert_accept(self):
        """弹出框确认"""
        try:
            alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
            alert.accept()
            self.test.debugLog("成功执行alert accept")
        except Exception as e:
            self.test.errorLog("无法执行alert accept")
            raise e

    def alert_input(self, text):
        """弹出框输入"""
        try:
            alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
            alert.send_keys(text)
            self.test.debugLog("成功执行alert input")
        except Exception as e:
            self.test.errorLog("无法执行alert input")
            raise e

    def alert_cancel(self):
        """弹出框取消"""
        try:
            alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
            alert.dismiss()
            self.test.debugLog("成功执行alert cancel")
        except Exception as e:
            self.test.errorLog("无法执行alert cancel")
            raise e

    def free_click(self):
        """鼠标单击"""
        try:
            ActionChains(self.driver).click().perform()
            self.test.debugLog("成功执行free click")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行free click")
            raise e

    def clear(self, element):
        """清空"""
        try:
            self.find_element(element).clear()
            self.test.debugLog("成功执行clear")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行clear")
            raise e

    def input_text(self, element, text):
        """输入"""
        try:
            self.find_element(element).send_keys(text)
            self.test.debugLog("成功执行文本输入:'%s'" % text)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行文本输入:'%s'" % text)
            raise e

    def click(self, element):
        """单击"""
        try:
            self.find_element(element).click()
            self.test.debugLog("成功执行click")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行click")
            raise e

    def submit(self, element):
        """提交"""
        try:
            self.find_element(element).submit()
            self.test.debugLog("成功执行submit")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行submit")
            raise e

    def click_and_hold(self, element):
        """单击保持"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).click_and_hold(ele).perform()
            self.test.debugLog("成功执行click and hold")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行click and hold")
            raise e

    def context_click(self, element):
        """右键点击"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).context_click(ele).perform()
            self.test.debugLog("成功执行context click")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行context click")
            raise e

    def double_click(self, element):
        """双击"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).double_click(ele).perform()
            self.test.debugLog("成功执行double click")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行double click")
            raise e

    def drag_and_drop(self, start_element, end_element):
        """拖拽"""
        try:
            ele = self.find_element(start_element)
            tar_ele = self.find_element(end_element)
            ActionChains(self.driver).drag_and_drop(ele, tar_ele).perform()
            self.test.debugLog("成功执行drag and drop to element")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行drag and drop to element")
            raise e

    def drag_and_drop_by_offset(self, element, x, y):
        """偏移拖拽"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).drag_and_drop_by_offset(ele, x, y).perform()
            self.test.debugLog("成功执行drag and drop to (%s, %s)" % (x,y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行drag and drop to (%s, %s)" % (x,y))
            raise e

    def key_down(self, element, value):
        """按下键位"""
        try:
            ele = self.find_element(element)
            if hasattr(Keys, value.upper()):
                keys = getattr(Keys, value)
            else:
                raise Exception("键位%s不存在" % value)
            ActionChains(self.driver).key_down(keys, ele).perform()
            self.test.debugLog("成功执行key down %s" % value)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行key down %s" % value)
            raise e

    def key_up(self, element, value):
        """释放键位"""
        try:
            ele = self.find_element(element)
            if hasattr(Keys, value.upper()):
                keys = getattr(Keys, value)
            else:
                raise Exception("键位%s不存在" % value)
            ActionChains(self.driver).key_up(keys, ele).perform()
            self.test.debugLog("成功执行key up %s" % value)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行key up %s" % value)
            raise e

    def move_by_offset(self, x, y):
        """鼠标移动到坐标"""
        try:
            ActionChains(self.driver).move_by_offset(x, y).perform()
            self.test.debugLog("成功执行move mouse to (%s, %s)" % (x,y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to (%s, %s)" % (x,y))
            raise e

    def move_to_element(self, element):
        """鼠标移动到元素"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.test.debugLog("成功执行move mouse to element")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to element")
            raise e

    def move_to_element_with_offset(self, element, x, y):
        """鼠标移动到元素坐标"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).move_to_element_with_offset(ele, x, y).perform()
            self.test.debugLog("成功执行move mouse to element with (%s, %s)" % (x,y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to element with (%s, %s)" % (x,y))
            raise e

    def release(self, element):
        """释放点击保持状态"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).release(ele).perform()
            self.test.debugLog("成功执行release mouse")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行release mouse")
            raise e

    def wait_element_appear(self, element, second):
        """等待元素出现"""
        try:
            WebDriverWait(self.driver, second, 0.2).until(expected_conditions.presence_of_element_located(element))
            self.test.debugLog("成功执行wait %ds until element appear" % second)
        except Exception as e:
            self.test.errorLog("无法执行wait %ds until element appear" % second)
            raise e

    def wait_element_disappear(self, element, second):
        """等待元素消失"""
        try:
            WebDriverWait(self.driver, second, 0.2).until_not(expected_conditions.presence_of_element_located(element))
            self.test.debugLog("成功执行wait %ds until element disappear" % second)
        except Exception as e:
            self.test.errorLog("无法执行wait %ds until element disappear" % second)
            raise e

    def custom(self, **kwargs):
        """自定义"""
        code = kwargs["code"]
        names = locals()
        names["element"] = kwargs["element"]
        names["data"] = kwargs["data"]
        names["driver"] = self.driver
        names["test"] = self.test
        try:
            exec(code)
            self.test.debugLog("成功执行 %s" % kwargs["trans"])
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
