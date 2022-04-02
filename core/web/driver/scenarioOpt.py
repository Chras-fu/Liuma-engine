from core.web.driver.operation import Operation


class Scenario(Operation):
    """场景类类操作"""

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
        except Exception as e:
            self.test.errorLog("无法执行 %s" % kwargs["trans"])
            raise e
