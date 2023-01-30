# -*- coding: utf-8 -*-
import os
import copy
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from requests import Session
import zipfile
from lm.lm_run import LMRun
from lm.lm_log import DebugLogger, ErrorLogger
from lm.lm_config import DATA_PATH, LMConfig
from lm.lm_api import LMApi


class LMSetting(object):
    def __init__(self, task):
        self.task = task
        self.data_path = DATA_PATH
        self.config = LMConfig()

    def data_pull(self):
        data_url = self.task["downloadUrl"]
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        try:
            file = LMApi().download_task_file(data_url)
        except Exception as e:
            ErrorLogger("数据拉取失败 错误信息: %s" % str(e))
            return None
        else:
            file_path = os.path.join(self.data_path, str(self.task["taskId"]) + ".zip")
            with open(file_path, 'wb+') as f:
                for chunk in file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            f.close()
            DebugLogger("数据拉取成功")
            return file_path

    def file_unzip(self, file_path):
        r = zipfile.is_zipfile(file_path)
        if r:
            with zipfile.ZipFile(file_path, 'r') as fz:
                for file in fz.namelist():
                    fz.extract(file, self.data_path)
        os.remove(file_path)

    def task_analysis(self):
        test_plan = {}
        if self.task["taskType"] != 'debug':
            file_path = self.data_pull()
            if file_path is not None:
                self.file_unzip(file_path)
            for collection_map in self.task["testCollectionList"]:
                collection = collection_map["collectionId"]
                test_case_list = collection_map["testCaseList"]
                session = LMSession()
                driver = LMDriver()
                context = dict()
                for case in test_case_list:
                    test_case = {
                        "driver": driver,
                        "session": session,
                        "context": context,
                        "task_id": self.task["taskId"],
                        "test_type": case["caseType"],
                        "test_class": "class_" + collection,
                        "test_case": "case_%s_%s" % (case["caseId"], case["index"]),
                        "test_data": os.path.join(self.data_path, self.task["taskId"], collection, case["caseId"] + ".json")
                    }
                    if collection not in test_plan.keys():
                        test_plan[collection] = []
                    test_plan[collection].append(test_case)
        else:
            collection_map = self.task["testCollectionList"][0]
            collection = collection_map["collectionId"]
            session = LMSession()
            driver = LMDriver()
            context = dict()
            test_case = {
                "driver": driver,
                "session": session,
                "context": context,
                "task_id": self.task["taskId"],
                "test_type": collection_map["testCaseList"][0]["caseType"],
                "test_class": "class_" + collection,
                "test_case": "case_%s_%s" % (collection_map["testCaseList"][0]["caseId"], collection_map["testCaseList"][0]["index"]),
                "test_data": self.task["debugData"]
            }
            test_plan[collection] = [test_case]
        return test_plan

    def create_thread(self, plan, queue, current_exec_status):
        runTime = 1
        if self.task["reRun"]:
            runTime = 2
        task_id = self.task["taskId"]
        max_thread = self.task["maxThread"]
        queue.put("run_all_start--%s" % task_id)
        for index in range(runTime):
            if index == 0:
                test_plan = plan
            else:
                test_plan = self.read_fail_case(test_plan, default_result)
            default_result = []
            if len(test_plan) > 0:
                queue.put("start_run_index--%s" % index)
                default_lock = threading.RLock()
                # 进行线程池管理执行 设置最大并发
                with ThreadPoolExecutor(max_workers=max_thread) as t:
                    executors = [t.submit(LMRun(test_case_list, index + 1, default_result, default_lock,
                                                queue).run_test, ) for test_case_list in test_plan.values()]
                    as_completed(executors)

        queue.put("run_all_stop--%s" % task_id)
        current_exec_status.value = 1

    @staticmethod
    def read_fail_case(test_plan, result):
        new_test_plan = copy.deepcopy(test_plan)
        for collection, test_case_list in new_test_plan.items():
            for test in test_case_list:
                case_id = test["test_case"].split("_")[1]
                index = test["test_case"].split("_")[-1]
                for case in result:
                    if case["collectionId"] == collection and case["caseId"] == case_id and case["index"] == int(index):
                        if case["status"] in (0, 3):
                            for old_test in test_plan[collection]:
                                if old_test["test_case"] == test["test_case"]:
                                    test_plan[collection].remove(old_test)
                                    break
                        result.remove(case)
                        break
            else:
                if len(test_plan[collection]) == 0:
                    del test_plan[collection]
        return test_plan

    
class LMSession(object):
    """API测试专用"""
    def __init__(self):
        self.session = Session()


class LMDriver(object):
    """WEB测试专用"""
    def __init__(self):
        self.driver = None
        self.config = LMConfig()
        self.browser_opt = self.config.browser_opt
        self.browser_path = self.config.browser_path

