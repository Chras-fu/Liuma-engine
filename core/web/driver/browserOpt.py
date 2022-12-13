from selenium.common.exceptions import NoSuchElementException

from core.web.driver import Operation
from datetime import datetime
from time import sleep

from tools.utils.utils import url_join


class Browser(Operation):
    """浏览器类操作"""

    def max_window(self):
        """最大化窗口"""
        try:
            self.driver.maximize_window()
            self.test.debugLog("成功执行maximize window")
        except Exception as e:
            self.test.errorLog("无法执行maximize window")
            raise e

    def min_window(self):
        """最小化窗口"""
        try:
            self.driver.minimize_window()
            self.test.debugLog("成功执行minimize window")
        except Exception as e:
            self.test.errorLog("无法执行minimize window")
            raise e

    def full_window(self):
        """全屏窗口"""
        try:
            self.driver.fullscreen_window()
            self.test.debugLog("成功执行full screen window")
        except Exception as e:
            self.test.errorLog("无法执行full screen window")
            raise e

    def set_position_window(self, x, y):
        """设置窗口位置"""
        """0,0是左上角"""
        try:
            self.driver.set_window_position(x, y)
            self.test.debugLog("成功执行set window position")
        except Exception as e:
            self.test.errorLog("无法执行set window position")
            raise e

    def set_size_window(self, width, height):
        """设置窗口大小"""
        try:
            self.driver.set_window_size(width, height)
            self.test.debugLog("成功执行set window size")
        except Exception as e:
            self.test.errorLog("无法执行set window size")
            raise e

    def switch_to_window(self, window):
        """切换窗口"""
        try:
            self.driver.switch_to.window(window)
            self.test.debugLog("成功执行switch window")
        except Exception as e:
            self.test.errorLog("无法执行switch window")
            raise e

    def close_window(self):
        """关闭窗口"""
        try:
            self.driver.close()
            self.test.debugLog("成功执行close window")
        except Exception as e:
            self.test.errorLog("无法执行close window")
            raise e

    def save_screenshot(self, name):
        """屏幕截图"""
        try:
            screenshot = self.driver.get_screenshot_as_png()
            self.test.saveScreenShot(name, screenshot)
            self.test.debugLog("成功执行screen shot")
        except Exception as e:
            self.test.errorLog("无法执行screen shot")
            raise e

    def click_to_new_window(self, element):
        """单击跳转新窗口"""
        try:
            current = self.driver.window_handles
            # 点击打开新窗口
            self.find_element(element).click()
            # 等待新窗口出现
            current_time = datetime.now()
            while (datetime.now()-current_time).seconds < 60:
                if len(self.driver.window_handles) > len(current):
                    for window_handle in self.driver.window_handles:
                        if window_handle not in current:
                            self.driver.switch_to.window(window_handle)
                            self.test.debugLog("成功执行click and switch to new window")
                            return
                else:
                    sleep(2)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行click and switch to new window")
            raise e

    def back_and_close_window(self, window):
        """返回并关闭当前窗口"""
        try:
            self.driver.close()
            self.driver.switch_to.window(window)
            self.test.debugLog("成功执行back and close window")
        except Exception as e:
            self.test.errorLog("无法执行back and close window")
            raise e

    def open_url(self, domain, path):
        """打开网页"""
        try:
            if domain is None:
                domain = ""
            url = url_join(domain, path)
            self.driver.get(url)
            self.driver.implicitly_wait(2)
            self.test.debugLog("成功打开 '%s'" % url_join(domain, path))
        except Exception as e:
            self.test.errorLog("无法打开 '%s'" % url_join(domain, path))
            raise e

    def refresh(self):
        """刷新页面"""
        try:
            self.driver.refresh()
            self.test.debugLog("成功执行refresh")
        except Exception as e:
            self.test.errorLog("无法执行refresh")
            raise e

    def back(self):
        """页面后退"""
        try:
            self.driver.back()
            self.test.debugLog("成功执行back")
        except Exception as e:
            self.test.errorLog("无法执行back")
            raise e

    def forward(self):
        """页面前进"""
        try:
            self.driver.forward()
            self.test.debugLog("成功执行forward")
        except Exception as e:
            self.test.errorLog("无法执行forward")
            raise e

    def add_cookie(self, name, value):
        """添加cookie"""
        try:
            self.driver.add_cookie({'name': name, 'value': value})
            self.test.debugLog("成功执行add cookie: %s:%s" % (name, value))
        except Exception as e:
            self.test.errorLog("无法执行add cookie: %s:%s" % (name, value))
            raise e

    def delete_cookie(self, name):
        """删除cookie"""
        try:
            self.driver.delete_cookie(name)
            self.test.debugLog("成功执行delete cookie:%s" % name)
        except Exception as e:
            self.test.errorLog("无法执行delete cookie:%s" % name)
            raise e

    def delete_cookies(self):
        """删除cookies"""
        try:
            self.driver.delete_all_cookies()
            self.test.debugLog("成功执行delete cookies")
        except Exception as e:
            self.test.errorLog("无法执行delete cookies")
            raise e

    def execute_script(self, script, arg:tuple):
        """执行脚本"""
        try:
            self.driver.execute_script(script, *arg)
            self.test.debugLog("成功执行execute script:%s" % script)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行execute script:%s" % script)
            raise e

    def execute_async_script(self, script, arg:tuple):
        """执行异步脚本"""
        try:
            self.driver.execute_async_script(script, *arg)
            self.test.debugLog("成功执行execute async script:%s" % script)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行execute async script:%s" % script)
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
            self.driver.implicitly_wait(second)
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
