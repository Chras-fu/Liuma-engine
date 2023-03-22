# -*- coding: utf-8 -*-
import datetime
import io
import sys
import unittest


class LMResult(unittest.TestResult):

    def __init__(self, result, lock, queue):
        unittest.TestResult.__init__(self)
        self.stdout_buffer = None
        self.original_stdout = sys.stdout
        self.default_result = result
        self.default_lock = lock
        self.queue = queue
        self.result = []

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.setupStdout()
        test.stdout_buffer = self.stdout_buffer
        test.start_time = datetime.datetime.now()

    def setupStdout(self):
        if self.stdout_buffer is None:
            self.stdout_buffer = io.StringIO()

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        test.stop_time = datetime.datetime.now()
        if self.default_lock.acquire():
            status, test_case, error = self.result[-1]
            case_info = {
                "status": status,
                "startTime": test_case.start_time.timestamp()*1000,
                "endTime": test_case.stop_time.timestamp()*1000,
                "collectionId": test_case.__class__.__doc__.split("_")[-1],
                "caseId": getattr(test, "case_name", " _ ").split("_")[1],
                "caseType": getattr(test, "case_type", "API"),
                "caseName": getattr(test, "test_case_name", "未知"),
                "caseDesc": getattr(test, "test_case_desc", None),
                "index": int(getattr(test, "case_name", " _0").split("_")[-1]),
                "runTimes": getattr(test, "run_index", 1),
                "transactionList": test_case.trans_list
            }
            self.default_result.append(case_info)
            self.queue.put(case_info)
            self.default_lock.release()

    def restoreStdout(self):
        self.stdout_buffer.seek(0)
        self.stdout_buffer.truncate()

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.mergeResult(0, test, "")

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        self.mergeResult(1, test, _exc_str)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        self.mergeResult(2, test, _exc_str)

    def addSkip(self, test, reason):
        unittest.TestResult.addSkip(self, test, reason)
        self.mergeResult(3, test, reason)

    def mergeResult(self, n, test, e):
        self.result.append((n, test, e))
