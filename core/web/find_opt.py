from core.web.driver.browserOpt import Browser
from core.web.driver.pageOpt import Page
from core.web.driver.scenarioOpt import Scenario
from core.web.driver.assertionOpt import Assertion
from core.web.driver.relationOpt import Relation
from core.web.driver.conditionOpt import Condition


def find_browser_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("最大化窗口")
    def max_window(test, driver, **kwargs):
        Browser(test, driver).max_window()

    @keywords("最小化窗口")
    def min_window(test, driver, **kwargs):
        Browser(test, driver).min_window()

    @keywords("全屏窗口")
    def full_window(test, driver, **kwargs):
        Browser(test, driver).full_window()

    @keywords("设置窗口位置")
    def set_position_window(test, driver, **kwargs):
        Browser(test, driver).set_position_window(kwargs["data"]["x"], kwargs["data"]["y"])

    @keywords("设置窗口大小")
    def set_size_window(test, driver, **kwargs):
        Browser(test, driver).set_size_window(kwargs["data"]["width"], kwargs["data"]["height"])

    @keywords("切换窗口")
    def switch_to_window(test, driver, **kwargs):
        Browser(test, driver).switch_to_window(kwargs["data"]["window"])

    @keywords("关闭窗口")
    def close_window(test, driver, **kwargs):
        Browser(test, driver).close_window()

    @keywords("屏幕截图")
    def save_screenshot(test, driver, **kwargs):
        Browser(test, driver).save_screenshot(kwargs["data"]["name"])

    @keywords("单击跳转新窗口")
    def click_to_new_window(test, driver, **kwargs):
        Browser(test, driver).click_to_new_window(kwargs["element"]["element"])

    @keywords("返回并关闭当前窗口")
    def back_and_close_window(test, driver, **kwargs):
        Browser(test, driver).back_and_close_window(kwargs["data"]["window"])

    @keywords("打开网页")
    def open_url(test, driver, **kwargs):
        Browser(test, driver).open_url(kwargs["data"]["domain"], kwargs["data"]["path"])

    @keywords("刷新")
    def refresh(test, driver, **kwargs):
        Browser(test, driver).refresh()

    @keywords("后退")
    def back(test, driver, **kwargs):
        Browser(test, driver).back()

    @keywords("前进")
    def forward(test, driver, **kwargs):
        Browser(test, driver).forward()

    @keywords("强制等待")
    def sleep(test, driver, **kwargs):
        Browser(test, driver).sleep(kwargs["data"]["second"])

    @keywords("隐式等待")
    def implicitly_wait(test, driver, **kwargs):
        Browser(test, driver).implicitly_wait(kwargs["data"]["second"])

    @keywords("添加cookie")
    def add_cookie(test, driver, **kwargs):
        Browser(test, driver).add_cookie(kwargs["data"]["name"], kwargs["data"]["value"])

    @keywords("删除cookie")
    def delete_cookie(test, driver, **kwargs):
        Browser(test, driver).delete_cookie(kwargs["data"]["name"])

    @keywords("删除cookies")
    def delete_cookies(test, driver, **kwargs):
        Browser(test, driver).delete_cookies()

    @keywords("执行脚本")
    def execute_script(test, driver, **kwargs):
        Browser(test, driver).execute_script(kwargs["data"]["script"], tuple(kwargs["data"]["arg"]))

    @keywords("执行异步脚本")
    def execute_async_script(test, driver, **kwargs):
        Browser(test, driver).execute_async_script(kwargs["data"]["script"], tuple(kwargs["data"]["arg"]))

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        Browser(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_page_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func
        return back

    @keywords("切换frame")
    def switch_frame(test, driver, **kwargs):
        Page(test, driver).switch_frame(kwargs["element"]["frame"])

    @keywords("返回默认frame")
    def switch_content(test, driver, **kwargs):
        Page(test, driver).switch_content()

    @keywords("返回父级frame")
    def switch_parent(test, driver, **kwargs):
        Page(test, driver).switch_parent()

    @keywords("弹出框确认")
    def alert_accept(test, driver, **kwargs):
        Page(test, driver).alert_accept()

    @keywords("弹出框输入")
    def alert_input(test, driver, **kwargs):
        Page(test, driver).alert_input(kwargs["data"]["text"])

    @keywords("弹出框取消")
    def alert_cancel(test, driver, **kwargs):
        Page(test, driver).alert_cancel()

    @keywords("鼠标单击")
    def click_and_hold(test, driver, **kwargs):
        Page(test, driver).free_click()

    @keywords("清空")
    def clear(test, driver, **kwargs):
        Page(test, driver).clear(kwargs["element"]["element"])

    @keywords("输入")
    def input(test, driver, **kwargs):
        Page(test, driver).input_text(kwargs["element"]["element"], kwargs["data"]["text"])

    @keywords("单击")
    def click(test, driver, **kwargs):
        Page(test, driver).click(kwargs["element"]["element"])

    @keywords("提交")
    def submit(test, driver, **kwargs):
        Page(test, driver).submit(kwargs["element"]["element"])

    @keywords("单击保持")
    def click_and_hold(test, driver, **kwargs):
        Page(test, driver).click_and_hold(kwargs["element"]["element"])

    @keywords("右键点击")
    def context_click(test, driver, **kwargs):
        Page(test, driver).context_click(kwargs["element"]["element"])

    @keywords("双击")
    def double_click(test, driver, **kwargs):
        Page(test, driver).double_click(kwargs["element"]["element"])

    @keywords("拖拽")
    def drag_and_drop(test, driver, **kwargs):
        Page(test, driver).drag_and_drop(kwargs["element"]["startElement"], kwargs["element"]["endElement"])

    @keywords("偏移拖拽")
    def drag_and_drop_by_offset(test, driver, **kwargs):
        Page(test, driver).drag_and_drop_by_offset(kwargs["element"]["element"], kwargs["data"]["x"], kwargs["data"]["y"])

    @keywords("按下键位")
    def key_down(test, driver, **kwargs):
        Page(test, driver).key_down(kwargs["element"]["element"], kwargs["data"]["value"])

    @keywords("释放键位")
    def key_up(test, driver, **kwargs):
        Page(test, driver).key_up(kwargs["element"]["element"], kwargs["data"]["value"])

    @keywords("鼠标移动到坐标")
    def move_by_offset(test, driver, **kwargs):
        Page(test, driver).move_by_offset(kwargs["data"]["x"], kwargs["data"]["y"])

    @keywords("鼠标移动到元素")
    def move_to_element(test, driver, **kwargs):
        Page(test, driver).move_to_element(kwargs["element"]["element"])

    @keywords("鼠标元素内偏移")
    def move_to_element_with_offset(test, driver, **kwargs):
        Page(test, driver).move_to_element_with_offset(kwargs["element"]["element"], kwargs["data"]["x"], kwargs["data"]["y"])

    @keywords("释放点击保持状态")
    def release(test, driver, **kwargs):
        Page(test, driver).release(kwargs["element"]["element"])

    @keywords("等待元素出现")
    def web_driver_wait(test, driver, **kwargs):
        Page(test, driver).wait_element_appear(kwargs["element"]["element"], kwargs["data"]["second"])

    @keywords("等待元素消失")
    def web_driver_wait(test, driver, **kwargs):
        Page(test, driver).wait_element_disappear(kwargs["element"]["element"], kwargs["data"]["second"])

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        Page(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_assertion_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("断言页面标题")
    def assert_page_title(test, driver, **kwargs):
        return Assertion(test, driver).assert_page_title(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言页面url")
    def assert_page_url(test, driver, **kwargs):
        return Assertion(test, driver).assert_page_url(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言页面源码")
    def assert_page_source(test, driver, **kwargs):
        return Assertion(test, driver).assert_page_source(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言元素文本")
    def assert_ele_text(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_text(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                       kwargs["data"]["expect"])

    @keywords("断言元素tag")
    def assert_ele_tag(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_tag(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                      kwargs["data"]["expect"])

    @keywords("断言元素尺寸")
    def assert_ele_size(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_size(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                       kwargs["data"]["expect"])

    @keywords("断言元素高度")
    def assert_ele_height(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_height(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                         kwargs["data"]["expect"])

    @keywords("断言元素宽度")
    def assert_ele_width(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_width(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                        kwargs["data"]["expect"])

    @keywords("断言元素位置")
    def assert_ele_location(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_location(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                           kwargs["data"]["expect"])

    @keywords("断言元素X坐标")
    def assert_ele_height(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_x(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                    kwargs["data"]["expect"])

    @keywords("断言元素Y坐标")
    def assert_ele_y(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_y(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                    kwargs["data"]["expect"])

    @keywords("断言元素属性")
    def assert_ele_attribute(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_attribute(kwargs["element"]["element"], kwargs["data"]["name"],
                                                            kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言元素是否选中")
    def assert_ele_selected(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_selected(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                           kwargs["data"]["expect"])

    @keywords("断言元素是否启用")
    def assert_ele_enabled(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_enabled(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                          kwargs["data"]["expect"])

    @keywords("断言元素是否显示")
    def assert_ele_displayed(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_displayed(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                            kwargs["data"]["expect"])

    @keywords("断言元素css样式")
    def assert_ele_css(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_css(kwargs["element"]["element"], kwargs["data"]["name"],
                                                      kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言元素是否存在")
    def assert_ele_existed(test, driver, **kwargs):
        return Assertion(test, driver).assert_ele_existed(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                          kwargs["data"]["expect"])

    @keywords("断言窗口位置")
    def assert_window_position(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_position(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言窗口X坐标")
    def assert_window_x(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_x(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言窗口Y坐标")
    def assert_window_y(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_y(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言窗口尺寸")
    def assert_window_size(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_size(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言窗口宽度")
    def assert_window_width(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_width(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言窗口高度")
    def assert_window_height(test, driver, **kwargs):
        return Assertion(test, driver).assert_window_height(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言cookies")
    def assert_cookies(test, driver, **kwargs):
        return Assertion(test, driver).assert_cookies(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("断言cookie")
    def assert_cookie(test, driver, **kwargs):
        return Assertion(test, driver).assert_cookie(kwargs["data"]["name"], kwargs["data"]["assertion"],
                                                     kwargs["data"]["expect"])

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        return Assertion(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_relation_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("提取页面标题")
    def get_page_title(test, driver, **kwargs):
        Relation(test, driver).get_page_title(kwargs["data"]["save_name"])

    @keywords("提取页面url")
    def get_page_url(test, driver, **kwargs):
        Relation(test, driver).get_page_url(kwargs["data"]["save_name"])

    @keywords("提取元素文本")
    def get_ele_text(test, driver, **kwargs):
        Relation(test, driver).get_ele_text(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素tag")
    def get_ele_tag(test, driver, **kwargs):
        Relation(test, driver).get_ele_tag(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素尺寸")
    def get_ele_size(test, driver, **kwargs):
        Relation(test, driver).get_ele_size(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素高度")
    def get_ele_height(test, driver, **kwargs):
        Relation(test, driver).get_ele_height(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素宽度")
    def get_ele_width(test, driver, **kwargs):
        Relation(test, driver).get_ele_width(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素位置")
    def get_ele_location(test, driver, **kwargs):
        Relation(test, driver).get_ele_location(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素X坐标")
    def get_ele_height(test, driver, **kwargs):
        Relation(test, driver).get_ele_x(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素Y坐标")
    def get_ele_y(test, driver, **kwargs):
        Relation(test, driver).get_ele_y(kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素属性")
    def get_ele_attribute(test, driver, **kwargs):
        Relation(test, driver).get_ele_attribute(kwargs["element"]["element"], kwargs["data"]["name"], kwargs["data"]["save_name"])

    @keywords("提取元素css样式")
    def get_ele_css(test, driver, **kwargs):
        Relation(test, driver).get_ele_css(kwargs["element"]["element"], kwargs["data"]["name"],
                                           kwargs["data"]["save_name"])

    @keywords("提取窗口位置")
    def get_window_position(test, driver, **kwargs):
        Relation(test, driver).get_window_position(kwargs["data"]["save_name"])

    @keywords("提取窗口X坐标")
    def get_window_x(test, driver, **kwargs):
        Relation(test, driver).get_window_x(kwargs["data"]["save_name"])

    @keywords("提取窗口Y坐标")
    def get_window_y(test, driver, **kwargs):
        Relation(test, driver).get_window_y(kwargs["data"]["save_name"])

    @keywords("提取窗口尺寸")
    def get_window_size(test, driver, **kwargs):
        Relation(test, driver).get_window_size(kwargs["data"]["save_name"])

    @keywords("提取窗口宽度")
    def get_window_width(test, driver, **kwargs):
        Relation(test, driver).get_window_width(kwargs["data"]["save_name"])

    @keywords("提取窗口高度")
    def get_window_height(test, driver, **kwargs):
        Relation(test, driver).get_window_height(kwargs["data"]["save_name"])

    @keywords("提取当前窗口句柄")
    def get_current_handle(test, driver, **kwargs):
        Relation(test, driver).get_current_handle(kwargs["data"]["save_name"])

    @keywords("提取所有窗口句柄")
    def get_all_handle(test, driver, **kwargs):
        Relation(test, driver).get_all_handle(kwargs["data"]["save_name"])

    @keywords("提取cookies")
    def get_cookies(test, driver, **kwargs):
        Relation(test, driver).get_cookies(kwargs["data"]["save_name"])

    @keywords("提取cookie")
    def get_cookie(test, driver, **kwargs):
        Relation(test, driver).get_cookie(kwargs["data"]["name"], kwargs["data"]["save_name"])

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        Relation(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_condition_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("判断页面标题")
    def condition_page_title(test, driver, **kwargs):
        return Condition(test, driver).condition_page_title(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断页面url")
    def condition_page_url(test, driver, **kwargs):
        return Condition(test, driver).condition_page_url(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断页面源码")
    def condition_page_source(test, driver, **kwargs):
        return Condition(test, driver).condition_page_source(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断元素文本")
    def condition_ele_text(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_text(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                          kwargs["data"]["expect"])

    @keywords("判断元素tag")
    def condition_ele_tag(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_tag(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                         kwargs["data"]["expect"])

    @keywords("判断元素尺寸")
    def condition_ele_size(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_size(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                          kwargs["data"]["expect"])

    @keywords("判断元素高度")
    def condition_ele_height(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_height(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                            kwargs["data"]["expect"])

    @keywords("判断元素宽度")
    def condition_ele_width(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_width(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                           kwargs["data"]["expect"])

    @keywords("判断元素位置")
    def condition_ele_location(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_location(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                              kwargs["data"]["expect"])

    @keywords("判断元素X坐标")
    def condition_ele_height(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_x(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                       kwargs["data"]["expect"])

    @keywords("判断元素Y坐标")
    def condition_ele_y(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_y(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                       kwargs["data"]["expect"])

    @keywords("判断元素属性")
    def condition_ele_attribute(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_attribute(kwargs["element"]["element"], kwargs["data"]["name"],
                                                               kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断元素是否选中")
    def condition_ele_selected(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_selected(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                              kwargs["data"]["expect"])

    @keywords("判断元素是否启用")
    def condition_ele_enabled(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_enabled(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                             kwargs["data"]["expect"])

    @keywords("判断元素是否显示")
    def condition_ele_displayed(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_displayed(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                               kwargs["data"]["expect"])

    @keywords("判断元素css样式")
    def condition_ele_css(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_css(kwargs["element"]["element"], kwargs["data"]["name"],
                                                         kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断元素是否存在")
    def condition_ele_existed(test, driver, **kwargs):
        return Condition(test, driver).condition_ele_existed(kwargs["element"]["element"], kwargs["data"]["assertion"],
                                                             kwargs["data"]["expect"])

    @keywords("判断窗口位置")
    def condition_window_position(test, driver, **kwargs):
        return Condition(test, driver).condition_window_position(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断窗口X坐标")
    def condition_window_x(test, driver, **kwargs):
        return Condition(test, driver).condition_window_x(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断窗口Y坐标")
    def condition_window_y(test, driver, **kwargs):
        return Condition(test, driver).condition_window_y(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断窗口尺寸")
    def condition_window_size(test, driver, **kwargs):
        return Condition(test, driver).condition_window_size(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断窗口宽度")
    def condition_window_width(test, driver, **kwargs):
        return Condition(test, driver).condition_window_width(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断窗口高度")
    def condition_window_height(test, driver, **kwargs):
        return Condition(test, driver).condition_window_height(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断cookies")
    def condition_cookies(test, driver, **kwargs):
        return Condition(test, driver).condition_cookies(kwargs["data"]["assertion"], kwargs["data"]["expect"])

    @keywords("判断cookie")
    def condition_cookie(test, driver, **kwargs):
        return Condition(test, driver).condition_cookie(kwargs["data"]["name"], kwargs["data"]["assertion"],
                                                        kwargs["data"]["expect"])

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        return Condition(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_scenario_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("自定义")
    def custom(test, driver, **kwargs):
        return Scenario(test, driver).custom(**kwargs)

    try:
        return function
    except:
        return None
