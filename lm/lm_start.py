# -*- coding: utf-8 -*-
import threading
from multiprocessing import Process, Queue, Value
import time, os, datetime
from lm.lm_api import LMApi
from lm.lm_setting import LMSetting
from lm.lm_report import LMReport
from lm.lm_log import DebugLogger, ErrorLogger
from lm.lm_config import LOG_PATH, IMAGE_PATH
from lm.lm_upload import LMUpload
import psutil
import inspect
import ctypes


def _async_raise(tid, exctype):
    """关闭线程方法"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        return False
    elif res == 0:
        return True
    else:
        return True


def stop_thread(thread):
    try:
        return _async_raise(thread.ident, SystemExit)
    except:
        return False


class LMStart(object):

    def __init__(self):
        self.api = LMApi()

    def main(self):
        """"启动入口"""
        exec_status = Value("i", 1)   # 执行状态 0 执行中、 1 待执行 默认待执行
        while True:
            retry = 0   # 关闭线程重试次数
            status_thread = threading.Thread(target=self.send_heartbeat)
            status_thread.start()
            task_queue = Queue()
            task_status_queue = Queue()
            task_thread = threading.Thread(target=self.get_task, args=(task_queue, task_status_queue, exec_status))
            task_thread.start()
            while retry < 3:    # 线程重试超过3次则默认线程需要重启
                if not status_thread.is_alive():
                    result = stop_thread(task_thread)
                    if result:
                        break
                    else:
                        retry += 1
                        continue
                if not task_thread.is_alive():
                    result = stop_thread(status_thread)
                    if result:
                        break
                    else:
                        retry += 1
                        continue
                try:
                    task = task_queue.get(True, 1)
                except Exception:
                    continue
                else:
                    DebugLogger("接受任务成功 启动执行进程")
                    case_result_queue = Queue()
                    current_exec_status = Value("i", 0)   # 0 执行中、 1 执行结束
                    run_process = Process(target=self.run_test, args=(task, case_result_queue, current_exec_status))
                    run_process.start()
                    report_process = Process(target=self.push_result, args=(exec_status, case_result_queue))
                    report_process.start()
                    upload_process = Process(target=self.upload_image, args=(task, current_exec_status))
                    upload_process.start()
                finally:
                    if not exec_status.value:
                        try:
                            task_status = task_status_queue.get(True, 0.05)
                        except Exception:
                            task_status = ""
                        finally:
                            try:
                                if task_status == "STOP":
                                    exec_status.value = 1
                                    if report_process.is_alive():
                                        report_process.terminate()
                                    if run_process.is_alive():
                                        for p in psutil.Process(run_process.pid).children():
                                            p.terminate()
                                        run_process.terminate()
                                    DebugLogger("引擎终止任务成功 任务id: %s" % task["taskId"])
                                    DebugLogger("-------------------------------------------------")
                                elif not report_process.is_alive():
                                    exec_status.value = 1
                                    if run_process.is_alive():
                                        for p in psutil.Process(run_process.pid).children():
                                            p.terminate()
                                        run_process.terminate()
                                elif not run_process.is_alive() and case_result_queue.empty():
                                    start_time = datetime.datetime.now()
                                    while (datetime.datetime.now() - start_time).seconds < 30:
                                        # 循环等待30s 防止最后一条结果数据没有发送出去 如果报告进程自销则中止等待
                                        if not report_process.is_alive():
                                            break
                                        time.sleep(3)
                                    exec_status.value = 1
                                    if report_process.is_alive():
                                        report_process.terminate()
                            except Exception as e:
                                ErrorLogger("关闭执行任务时发生错误 错误信息为：%s" % e)

    def send_heartbeat(self):
        log_path = os.path.join(LOG_PATH, "engine_status.log")
        while True:
            DebugLogger("-------------------------------------------------", file_path=log_path)
            DebugLogger("发送心跳", file_path=log_path)
            DebugLogger("-------------------------------------------------", file_path=log_path)
            self.api.send_heartbeat(log_path)
            time.sleep(60)

    def get_task(self, task_queue, task_status_queue, status):
        while True:
            if status.value:
                task = self.api.fetch_task()
                if task:
                    DebugLogger("-------------------------------------------------")
                    DebugLogger("引擎获取任务成功 任务id: %s" % (task["taskId"]))
                    task_queue.put(task)
                    status.value = 0
            else:
                data = self.api.get_task_status(task["taskId"])
                if data:
                    task_status_queue.put(data)
            time.sleep(3)

    @staticmethod
    def run_test(task, queue, current_exec_status):
        s = LMSetting(task)
        plan = s.task_analysis()
        s.create_thread(plan, queue, current_exec_status)

    @staticmethod
    def push_result(exec_status, case_result_queue):
        report = LMReport(exec_status, case_result_queue)
        report.monitor_result()

    @staticmethod
    def upload_image(task, current_exec_status):
        log_path = os.path.join(LOG_PATH, "engine_image.log")
        current_process = psutil.Process(os.getpid())
        task_image_path = os.path.join(IMAGE_PATH, task["taskId"])
        if not os.path.exists(task_image_path):
            os.makedirs(task_image_path)
        while True:
            if current_process.parent() is None:
                current_process.kill()
            files = os.listdir(task_image_path)
            if len(files) > 0:
                DebugLogger("-------------------------------------------------", file_path=log_path)
                DebugLogger("上传截图", file_path=log_path)
                LMUpload(files, log_path).set_upload(task_image_path)
                DebugLogger("-------------------------------------------------", file_path=log_path)
            else:
                if current_exec_status.value:
                    os.rmdir(task_image_path)
                    current_process.terminate()
            time.sleep(1)
