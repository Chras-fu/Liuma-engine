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

    @keywords("左滑屏幕")
    def open_app(test, device, **kwargs):
        System(test, device).open_app(kwargs["system"], kwargs["data"]["appId"], kwargs["data"]["activity"])

    @keywords("右滑屏幕")
    def open_app(test, device, **kwargs):
        System(test, device).open_app(kwargs["system"], kwargs["data"]["appId"], kwargs["data"]["activity"])

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

    @keywords("点击")
    def switch_frame(test, device, **kwargs):
        View(test, device).click()

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

    @keywords("断言页面标题")
    def assert_page_title(test, device, **kwargs):
        return Assertion(test, device).assert_page_title(kwargs["data"]["assertion"], kwargs["data"]["expect"])

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

    @keywords("提取页面标题")
    def get_page_title(test, device, **kwargs):
        Relation(test, device).get_page_title(kwargs["data"]["save_name"])

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

    @keywords("判断页面标题")
    def condition_page_title(test, device, **kwargs):
        return Condition(test, device).condition_page_title(kwargs["data"]["assertion"], kwargs["data"]["expect"])

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
