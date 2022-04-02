# -*- coding: utf-8 -*-
import datetime
import sys
import unittest


class LMResult(unittest.TestResult):

    def __init__(self, result, lock, queue, verbosity=1):
        unittest.TestResult.__init__(self)
        self.verbosity = verbosity
        self.default_result = result
        self.default_lock = lock
        self.queue = queue
        self.result = []

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        test.start_time = datetime.datetime.now()

    def stopTest(self, test):
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

    def printResult(self, n, test):
        name = test.case_name
        if self.verbosity > 1:
            if n == 0:  sys.stderr.write('Pass  ' + name + ' '  + '\n')
            if n == 1:  sys.stderr.write('Fail  ' + name + ' '  + '\n')
            if n == 2:  sys.stderr.write('Error  ' + name + ' ' + '\n')
            if n == 3:  sys.stderr.write('Skip  ' + name + ' '  + '\n')
        else:
            if n == 0:  sys.stderr.write('Pass')
            if n == 1:  sys.stderr.write('Fail')
            if n == 2:  sys.stderr.write('Error')
            if n == 3:  sys.stderr.write('Skip')
        sys.stderr.flush()
