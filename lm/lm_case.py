# -*- coding: utf-8 -*-
import os
import datetime
import unittest
import traceback
from uuid import uuid1
from core.api.testcase import ApiTestCase
from core.web.testcase import WebTestCase
# from core.app.testcase import AppTestCase
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
        # else:
        #     AppTestCase(test=self).execute()

    def doCleanups(self):
        unittest.TestCase.doCleanups(self)
        self.handleResult()

    def debugLog(self, log_info):
        """执行日志"""
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
        """错误日志"""
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
        """记录事务时长"""
        if len(self.trans_list) > 0:
            self.trans_list[-1]["during"] = during

    def defineTrans(self, id, name, content=""):
        """定义事务"""
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

    def deleteTrans(self, index):
        """删除事务"""
        if len(self.trans_list) > index:
            del self.trans_list[index]

    def updateTransStatus(self, status):
        if len(self.trans_list) > 0:
            self.trans_list[-1]["status"] = status

    def recordFailStatus(self, exc_info=None):
        """记录断言失败"""
        self._outcome.errors.append((self, exc_info))
        if len(self.trans_list) > 0:
            self.trans_list[-1]["status"] = 1  # 记录当前事务为失败
            self.errorLog(str(exc_info[1]))

    def recordErrorStatus(self, exc_info=None):
        """记录程序错误"""
        self._outcome.errors.append((self, exc_info))
        if len(self.trans_list) > 0:
            self.trans_list[-1]["status"] = 2  # 记录当前事务为错误
            self.errorLog(str(exc_info[1]))
            if LMConfig().enable_stderr.lower() == "true":
                # 此处可以打印详细报错的代码
                tb_e = traceback.TracebackException(exc_info[0], exc_info[1], exc_info[2])
                msg_lines = list(tb_e.format())
                err_msg = "程序错误信息: "
                for msg in msg_lines:
                    err_msg = err_msg + "<br>" + msg
                self.errorLog(str(err_msg))

    def saveScreenShot(self, name, screen_shot):
        """保存截图"""
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
        """结果处理"""
        if len(self.trans_list) == 0:
            self.defineTrans(self.case_name.split("_")[1], "未知")
        isFail = False
        isError = False
        error_type = None
        error_value = None
        error_tb = None
        # 处理用例执行过程中的错误和失败 以此来判断用例最终状态
        for index, (test, exc_info) in enumerate(self._outcome.errors):
            if exc_info is not None:
                if issubclass(exc_info[0], AssertionError):
                    isFail = True
                    if not isError:  # 默认错误优先级高
                        error_type = AssertionError
                        error_value = exc_info[1]
                        error_tb = exc_info[2]
                else:
                    isError = True
                    error_type = exc_info[0]
                    error_value = exc_info[1]
                    error_tb = exc_info[2]
        # 根据用例原始成功状态来判断最后一个事务是否是成功的
        if self._outcome.success is True:
            if self.trans_list[-1]["status"] == "":  # 如果最后一个事务没有状态，则设为pass
                self.trans_list[-1]["status"] = 0
            if isError or isFail:  # 有错误或者失败的话用例修改状态
                self._outcome.errors.clear()
                self._outcome.errors.append((self, (error_type, error_value, error_tb)))
                self._outcome.success = False
        else:
            # 如果用例原始成功状态为否 则说明最后一个事务是失败或者错误的
            exc_info = self._outcome.errors[-2][-1]  # 倒数第二个errors是最后一个事务的
            if issubclass(exc_info[0], AssertionError):
                self.trans_list[-1]["status"] = 1  # 最后一步设为fail
            else:
                self.errorLog(str(exc_info[1]))
                self.trans_list[-1]["status"] = 2  # 最后一步设为error
                if LMConfig().enable_stderr.lower() == "true":
                    # 此处可以打印详细报错的代码
                    tb_e = traceback.TracebackException(exc_info[0], exc_info[1], exc_info[2])
                    msg_lines = list(tb_e.format())
                    err_msg = "程序错误信息: "
                    for msg in msg_lines:
                        err_msg = err_msg + "<br>" + msg
                    self.errorLog(str(err_msg))
            self._outcome.errors.clear()
            self._outcome.errors.append((self, (error_type, error_value, error_tb)))
