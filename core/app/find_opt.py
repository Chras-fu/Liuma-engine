from core.app.device.viewOpt import View
from core.app.device.systemOpt import System
from core.app.device.scenarioOpt import Scenario
from core.app.device.assertionOpt import Assertion
from core.app.device.relationOpt import Relation
from core.app.device.conditionOpt import Condition


def find_system_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func

        return back

    @keywords("启动应用")
    def start_app(test, device, **kwargs):
        System(test, device).start_app(kwargs["data"]["appId"])

    @keywords("关闭应用")
    def close_app(test, device, **kwargs):
        System(test, device).close_app(kwargs["data"]["appId"])

    @keywords("左滑")
    def swipe_left(test, device, **kwargs):
        System(test, device).swipe_left(kwargs["system"])

    @keywords("右滑")
    def swipe_right(test, device, **kwargs):
        System(test, device).swipe_right(kwargs["system"])

    @keywords("上滑")
    def swipe_up(test, device, **kwargs):
        System(test, device).swipe_up(kwargs["system"])

    @keywords("下滑")
    def swipe_down(test, device, **kwargs):
        System(test, device).swipe_down(kwargs["system"])

    @keywords("系统首页")
    def home(test, device, **kwargs):
        System(test, device).home(kwargs["system"])

    @keywords("系统返回")
    def back(test, device, **kwargs):
        System(test, device).back()

    @keywords("系统按键")
    def press(test, device, **kwargs):
        System(test, device).press(kwargs["data"]["keycode"])

    @keywords("屏幕截图")
    def screenshot(test, device, **kwargs):
        System(test, device).screenshot(kwargs["data"]["name"])

    @keywords("亮屏")
    def screen_on(test, device, **kwargs):
        System(test, device).screen_on(kwargs["system"])

    @keywords("息屏")
    def screen_off(test, device, **kwargs):
        System(test, device).screen_off(kwargs["system"])

    @keywords("强制等待")
    def sleep(test, device, **kwargs):
        System(test, device).sleep(kwargs["data"]["second"])

    @keywords("隐式等待")
    def implicitly_wait(test, device, **kwargs):
        System(test, device).implicitly_wait(kwargs["data"]["second"])

    @keywords("自定义")
    def custom(test, device, **kwargs):
        System(test, device).custom(**kwargs)

    try:
        return function
    except:
        return None


def find_view_opt(operate_name: str):
    function = None

    def keywords(name):
        def back(func):
            if name == operate_name:
                nonlocal function
                function = func
        return back

    @keywords("单击")
    def click(test, device, **kwargs):
        View(test, device).click(kwargs["element"]["element"])

    @keywords("双击")
    def double_click(test, device, **kwargs):
        View(test, device).double_click(kwargs["system"], kwargs["element"]["element"])

    @keywords("长按")
    def long_click(test, device, **kwargs):
        View(test, device).long_click(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["second"])

    @keywords("坐标单击")
    def click_coord(test, device, **kwargs):
        View(test, device).click_coord(**kwargs["data"])

    @keywords("坐标双击")
    def double_click_coord(test, device, **kwargs):
        View(test, device).double_click_coord(kwargs["system"], **kwargs["data"])

    @keywords("坐标长按")
    def long_click_coord(test, device, **kwargs):
        View(test, device).long_click_coord(kwargs["system"], **kwargs["data"])

    @keywords("坐标滑动")
    def swipe_int(test, device, **kwargs):
        View(test, device).swipe(kwargs["system"], **kwargs["data"])

    @keywords("输入")
    def input_text(test, device, **kwargs):
        View(test, device).input_text(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["text"])

    @keywords("清空")
    def input_text(test, device, **kwargs):
        View(test, device).clear_text(kwargs["element"]["element"])

    @keywords("滑动到元素出现")
    def scroll_to_ele(test, device, **kwargs):
        View(test, device).scroll_to_ele(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["direction"])

    @keywords("缩小")
    def pinch_in(test, device, **kwargs):
        View(test, device).pinch_in(kwargs["system"], kwargs["element"]["element"])

    @keywords("放大")
    def pinch_out(test, device, **kwargs):
        View(test, device).pinch_out(kwargs["system"], kwargs["element"]["element"])

    @keywords("等待元素出现")
    def wait(test, device, **kwargs):
        View(test, device).wait(kwargs["element"]["element"], kwargs["data"]["second"])

    @keywords("等待元素消失")
    def wait_gone(test, device, **kwargs):
        View(test, device).wait_gone(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["second"])

    @keywords("拖动到元素")
    def drag_to_ele(test, device, **kwargs):
        View(test, device).drag_to_ele(kwargs["element"]["startElement"],kwargs["element"]["endElement"])

    @keywords("拖动到坐标")
    def drag_to_coord(test, device, **kwargs):
        View(test, device).drag_to_coord(kwargs["element"]["element"], **kwargs["data"])

    @keywords("坐标拖动")
    def drag_coord(test, device, **kwargs):
        View(test, device).drag_coord(**kwargs["data"])

    @keywords("元素内滑动")
    def swipe_ele(test, device, **kwargs):
        View(test, device).swipe_ele(kwargs["element"]["element"], kwargs["data"]["direction"])

    @keywords("等待弹框出现")
    def alert_wait(test, device, **kwargs):
        View(test, device).alert_wait(kwargs["data"]["second"])

    @keywords("弹框确认")
    def alert_accept(test, device, **kwargs):
        View(test, device).alert_accept()

    @keywords("弹框取消")
    def alert_dismiss(test, device, **kwargs):
        View(test, device).alert_dismiss()

    @keywords("弹框点击")
    def alert_click(test, device, **kwargs):
        View(test, device).alert_click(kwargs["data"]["name"])

    @keywords("自定义")
    def custom(test, device, **kwargs):
        View(test, device).custom(**kwargs)

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

    @keywords("断言元素存在")
    def assert_ele_exists(test, device, **kwargs):
        return Assertion(test, device).assert_ele_exists(kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言元素文本")
    def assert_ele_text(test, device, **kwargs):
        return Assertion(test, device).assert_ele_text(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言元素属性")
    def assert_ele_attribute(test, device, **kwargs):
        return Assertion(test, device).assert_ele_attribute(kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言元素位置")
    def assert_ele_center(test, device, **kwargs):
        return Assertion(test, device).assert_ele_center(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言元素X坐标")
    def assert_ele_x(test, device, **kwargs):
        return Assertion(test, device).assert_ele_x(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言元素Y坐标")
    def assert_ele_y(test, device, **kwargs):
        return Assertion(test, device).assert_ele_y(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("断言弹框存在")
    def assert_alert_exists(test, device, **kwargs):
        return Assertion(test, device).assert_alert_exists(**kwargs["data"])

    @keywords("断言弹框文本")
    def assert_alert_text(test, device, **kwargs):
        return Assertion(test, device).assert_alert_text(**kwargs["data"])

    @keywords("自定义")
    def custom(test, device, **kwargs):
        return Assertion(test, device).custom(**kwargs)

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

    @keywords("提取屏幕尺寸")
    def get_window_size(test, device, **kwargs):
        Relation(test, device).get_window_size(kwargs["system"], kwargs["data"]["save_name"])

    @keywords("提取屏幕宽度")
    def get_window_width(test, device, **kwargs):
        Relation(test, device).get_window_width(kwargs["system"], kwargs["data"]["save_name"])

    @keywords("提取屏幕高度")
    def get_window_height(test, device, **kwargs):
        Relation(test, device).get_window_height(kwargs["system"], kwargs["data"]["save_name"])

    @keywords("提取元素文本")
    def get_ele_text(test, device, **kwargs):
        Relation(test, device).get_ele_text(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素位置")
    def get_ele_center(test, device, **kwargs):
        Relation(test, device).get_ele_center(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素X坐标")
    def get_ele_x(test, device, **kwargs):
        Relation(test, device).get_ele_x(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取元素Y坐标")
    def get_ele_y(test, device, **kwargs):
        Relation(test, device).get_ele_y(kwargs["system"], kwargs["element"]["element"], kwargs["data"]["save_name"])

    @keywords("提取弹框文本")
    def get_alert_text(test, device, **kwargs):
        Relation(test, device).get_alert_text(kwargs["data"]["save_name"])

    @keywords("自定义")
    def custom(test, device, **kwargs):
        Relation(test, device).custom(**kwargs)

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

    @keywords("判断元素存在")
    def condition_ele_exists(test, device, **kwargs):
        return Condition(test, device).condition_ele_exists(kwargs["element"]["element"], **kwargs["data"])

    @keywords("判断元素文本")
    def condition_ele_text(test, device, **kwargs):
        return Condition(test, device).condition_ele_text(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("判断元素属性")
    def condition_ele_attribute(test, device, **kwargs):
        return Condition(test, device).condition_ele_attribute(kwargs["element"]["element"], **kwargs["data"])

    @keywords("判断元素位置")
    def condition_ele_center(test, device, **kwargs):
        return Condition(test, device).condition_ele_center(kwargs["system"], kwargs["element"]["element"],
                                                         **kwargs["data"])

    @keywords("判断元素X坐标")
    def condition_ele_x(test, device, **kwargs):
        return Condition(test, device).condition_ele_x(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("判断元素Y坐标")
    def condition_ele_y(test, device, **kwargs):
        return Condition(test, device).condition_ele_y(kwargs["system"], kwargs["element"]["element"], **kwargs["data"])

    @keywords("判断弹框存在")
    def condition_alert_exists(test, device, **kwargs):
        return Condition(test, device).condition_alert_exists(**kwargs["data"])

    @keywords("判断弹框文本")
    def condition_alert_text(test, device, **kwargs):
        return Condition(test, device).condition_alert_text(**kwargs["data"])

    @keywords("自定义")
    def custom(test, device, **kwargs):
        return Condition(test, device).custom(**kwargs)

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
    def custom(test, device, **kwargs):
        return Scenario(test, device).custom(**kwargs)

    try:
        return function
    except:
        return None
