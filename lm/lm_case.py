# -*- coding: utf-8 -*-
import os
import datetime
import unittest
import traceback
from uuid import uuid1
from core.api.testcase import ApiTestCase
from core.web.testcase import WebTestCase
from lm.lm_config import IMAGE_PATH, LMConfig


class LMCase(unittest.TestCase):

    def __init__(self, case_name, test_data, case_type="API"):
        self.test_data = test_data
        self.trans_list = []
        self.case_name = case_name
        self.case_type = case_type
        unittest.TestCase.__init__(self, case_name)

    def testEntrance(self):
        if self.case_type == "API":
            ApiTestCase(test=self).execute()
        elif self.case_type == "WEB":
            WebTestCase(test=self).execute()

    def doCleanups(self):
        unittest.TestCase.doCleanups(self)
        self.handleResult()

    def debugLog(self, log_info):
        if len(self.trans_list) > 0:
            current_time = datetime.datetime.now()
            log = "%s - Debug - %s" % (current_time.strftime('%Y-%m-%d %H:%M:%S.%f'), log_info)
            if self.trans_list[-1]["log"] != "":
                if self.case_type == "API":
                    log = "<br><br>" + log
                else:
                    log = "<br>" + log
            self.trans_list[-1]["log"] = self.trans_list[-1]["log"] + log

    def errorLog(self, log_info):
        if len(self.trans_list) > 0:
            current_time = datetime.datetime.now()
            log = "%s - Error - %s" % (current_time.strftime('%Y-%m-%d %H:%M:%S.%f'), log_info)
            if self.trans_list[-1]["log"] != "":
                if self.case_type == "API":
                    log = "<br><br>" + log
                else:
                    log = "<br>" + log
            self.trans_list[-1]["log"] = self.trans_list[-1]["log"] + log

    def recordTransDuring(self, during):
        if len(self.trans_list) > 0:
            self.trans_list[-1]["during"] = during

    def defineTrans(self, id, name, content=""):
        trans_dict = {
            "id": id,
            "name": name,
            "content": content,
            "log": "",
            "during": 0,
            "status": "",
            "screenShotList": []
        }
        self.trans_list.append(trans_dict)
        if len(self.trans_list) > 1 and self.trans_list[-2]["status"] == "":
            self.trans_list[-2]["status"] = 0

    def recordFailStatus(self, exc_info=None):
        """记录错误状态"""
        self._outcome.errors.append((self, exc_info))
        if len(self.trans_list) > 0:
            self.trans_list[-1]["status"] = 1

    def saveScreenShot(self, name, screen_shot):
        uuid = str(uuid1())
        task_id = getattr(self, "task_id")
        task_image_path = os.path.join(IMAGE_PATH, task_id)
        try:
            filename = "%s.png" % uuid
            if not os.path.exists(task_image_path):
                os.makedirs(task_image_path)
            file_path = os.path.join(task_image_path, filename)
            with open(file_path, 'wb') as f:
                f.write(screen_shot)
        except:
            self.errorLog("Fail: Failed to save screen shot %s" % name)
        else:
            if len(self.trans_list) > 0:
                self.trans_list[-1]["screenShotList"].append(uuid)

    def handleResult(self):
        if len(self.trans_list) == 0:
            self.defineTrans(self.case_name.split("_")[1], "未知")
        if self._outcome.success is True:
            isFail = False
            error_value = None
            error_tb = None
            for index, (test, exc_info) in enumerate(self._outcome.errors):
                if exc_info is not None:
                    isFail = True
                    error_value = exc_info[1]
                    error_tb = exc_info[2]
            if isFail is True:
                self._outcome.errors.clear()
                self._outcome.errors.append((self, (AssertionError, error_value, error_tb)))
                self._outcome.success = False
            if self.trans_list[-1]["status"] == "":
                self.trans_list[-1]["status"] = 0
        else:
            isError = False
            error_type = AssertionError
            error_value = None
            error_tb = None
            for index, (test, exc_info) in enumerate(self._outcome.errors):
                if exc_info is not None:
                    if issubclass(exc_info[0], self.failureException):
                        pass
                    else:
                        error_type = exc_info[0]
                        isError = True
                    error_value = exc_info[1]
                    error_tb = exc_info[2]
            self._outcome.errors.clear()
            self._outcome.errors.append((self, (error_type, error_value, error_tb)))
            if isError is True:
                if LMConfig().enable_stderr.lower() == "true":
                    # 此处可以打印详细报错的代码
                    tb_e = traceback.TracebackException(error_type, error_value, error_tb)
                    msg_lines = list(tb_e.format())
                    err_msg = "程序错误信息: "
                    for msg in msg_lines:
                        err_msg = err_msg + "<br>" + msg
                    self.errorLog(str(err_msg))
            if isError is True:
                self.errorLog(str(error_value))
                self.trans_list[-1]["status"] = 2
            else:
                self.trans_list[-1]["status"] = 1
