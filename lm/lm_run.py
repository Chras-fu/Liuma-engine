# -*- coding: utf-8 -*-
import unittest, threading
from lm import lm_case, lm_result
from lm.lm_log import ErrorLogger
from lm.lm_config import LMConfig


class LMRun(object):
    def __init__(self, plan_tuple, run_index, default_result, default_lock, queue, verbosity=2):
        self.plan_tuple = plan_tuple
        self.run_index = run_index
        self.default_result = default_result
        self.default_lock = default_lock
        self.queue = queue
        self.verbosity = verbosity

    def run_test(self):
        suite = unittest.TestSuite()
        for case in self.plan_tuple:
            cls_name = case["test_class"]
            try:
                cls = eval(cls_name)
            except:
                cls = type(cls_name, (lm_case.LMCase,), {'__doc__': cls_name})
            case_name = case["test_case"]
            case_type = case["test_type"]
            setattr(cls, case_name, lm_case.LMCase.testEntrance)
            case_data = case["test_data"]
            test_case = cls(case_name, case_data, case_type)
            test_case.task_id = case["task_id"]
            test_case.driver = case["driver"]
            test_case.session = case["session"]
            test_case.context = case["context"]
            test_case.run_index = self.run_index
            suite.addTest(test_case)

        result = lm_result.LMResult(self.default_result, self.default_lock, self.queue, verbosity=self.verbosity)

        try:
            suite(result)
            # 执行测试用例
        except Exception as ex:
            ErrorLogger("Failed to run test(RunTime:run%s & ThreadName:%s), Error info:%s" %
                        (self.run_index, threading.current_thread().name, ex))
