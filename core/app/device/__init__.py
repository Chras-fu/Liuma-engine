from typing import Optional

from uiautomator2 import Device
from wda import Client, AlertAction, WDAEmptyResponseError


class AndroidDriver(Device):
    """安卓设备"""
    def __call__(self, **kwargs):
        if len(kwargs) == 1 and "xpath" in kwargs:
            return self.xpath(kwargs["xpath"])
        else:
            return Device.__call__(self, **kwargs)

    def find_element(self, **kwargs):
        if len(kwargs) == 1 and "xpath" in kwargs:
            return self.xpath(kwargs["xpath"])
        else:
            return Device.__call__(self, **kwargs)


class AppleDevice(Client):
    """苹果设备"""

    def session(self,
                bundle_id=None,
                arguments: Optional[list] = None,
                environment: Optional[dict] = None,
                alert_action: Optional[AlertAction] = None):
        capabilities = {}
        if bundle_id:
            always_match = {
                "bundleId": bundle_id,
                "arguments": arguments or [],
                "environment": environment or {},
                "shouldWaitForQuiescence": False,
            }
            if alert_action:
                assert alert_action in ["accept", "dismiss"]
                capabilities["defaultAlertAction"] = alert_action

            capabilities['alwaysMatch'] = always_match

        payload = {
            "capabilities": capabilities,
            "desiredCapabilities": capabilities.get('alwaysMatch',
                                                    {}),  # 兼容旧版的wda
        }

        # when device is Locked, it is unable to start app
        if self.locked():
            self.unlock()

        try:
            res = self.http.post('session', payload)
        except WDAEmptyResponseError:
            """ when there is alert, might be got empty response
            use /wda/apps/state may still get sessionId
            """
            res = self.session().app_state(bundle_id)
            if res.value != 4:
                raise
        client = AppleDevice(self.__wda_url, _session_id=res.sessionId)
        client.__timeout = self.__timeout
        client.__callbacks = self.__callbacks
        return client

    def find_element(self, **kwargs):
        return self.__call__(self, **kwargs)


def connect_device(system: str, url: str):
    if system.lower() == "android":
        return AndroidDriver(url)
    else:
        return AppleDevice(url)


class Operation(object):
    def __init__(self, test, device):
        self.device = device
        self.test = test

    def find_element(self, ele):
        """查找单个元素"""
        try:
            element = self.device.find_element(**ele)
            self.test.debugLog("成功定位元素 'By: %s Expression: %s'" % ele)
            return element
        except Exception as e:
            self.test.errorLog("无法定位元素 'By: %s Expression: %s'" % ele)
            raise e

