# -*- coding: utf-8 -*-
import threading
from multiprocessing import Process, Queue, Value
import time, os
from lm.lm_api import LMApi
from lm.lm_setting import LMSetting
from lm.lm_report import LMReport
from lm.lm_log import DebugLogger, ErrorLogger
from lm.lm_config import LOG_PATH, IMAGE_PATH, LMConfig
from lm.lm_upload import LMUpload
import psutil
from lm.lm_ws import Client


class LMStart(object):

    def __init__(self):
        self.api = LMApi()
        self.config = LMConfig()
        self.exec_processes = {}

    def main(self):
        """"启动入口"""
        message_queue = Queue()     # 消息队列
        status_thread = threading.Thread(target=self.send_heartbeat, args=(message_queue,))
        status_thread.start()   # 启动心跳链接
        task_queue = Queue()    # 任务队列
        task_thread = threading.Thread(target=self.fetch_task, args=(task_queue,))
        task_thread.start()  # 启动拉取任务 初始化一次 避免任务遗漏
        monitor_thread = threading.Thread(target=self.monitor_message, args=(message_queue, task_queue))
        monitor_thread.start()     # 启动消息监听
        while True:
            try:
                task = task_queue.get(True, 1)
            except:
                continue
            else:
                DebugLogger("接受任务成功 启动执行进程 任务id: %s" % task["taskId"])
                case_result_queue = Queue()
                current_exec_status = Value("i", 0)  # 0 执行中、 1 执行结束
                run_process = Process(target=self.run_test, args=(task, case_result_queue, current_exec_status))
                run_process.start()
                report_process = Process(target=self.push_result, args=(message_queue, case_result_queue))
                report_process.start()
                upload_process = Process(target=self.upload_image, args=(task, current_exec_status))
                upload_process.start()
                self.exec_processes[task["taskId"]] = [run_process, report_process, upload_process]     # 保存当前进程

    def send_heartbeat(self, queue):
        while True:
            log_path = os.path.join(LOG_PATH, "engine_status.log")
            domain = self.config.url[:-1] if self.config.url.endswith("/") else self.config.url
            url = domain.replace("http", "ws") + "/websocket/engine/heartbeat?engineCode={}&engineSecret={}". \
                format(self.config.engine, self.config.secret)
            try:
                ws = Client(url, queue)
                ws.connect()
                while True:
                    time.sleep(30)
                    ws.send(bytes(0))   # 每隔30秒更新心跳
                    DebugLogger("-------------------------------------------------", file_path=log_path)
                    DebugLogger("心跳更新成功", file_path=log_path)
                    DebugLogger("-------------------------------------------------", file_path=log_path)
            except KeyboardInterrupt:
                ws.close()
            except Exception as e:
                DebugLogger("-------------------------------------------------", file_path=log_path)
                ErrorLogger("心跳连接失败 1秒钟后重试 失败原因%s" % e, file_path=log_path)
                DebugLogger("-------------------------------------------------", file_path=log_path)
            time.sleep(1)

    def fetch_task(self, queue):
        while True:
            if len(self.exec_processes) < int(self.config.max_run):
                task = self.api.fetch_task()
                if task:
                    self.exec_processes[task["taskId"]] = []
                    DebugLogger("引擎获取任务成功 任务id: %s" % (task["taskId"]))
                    queue.put(task)
                else:   # 没有任务 停止获取
                    break
            else:
                time.sleep(3)

    def monitor_message(self, message_queue, task_queue):
        while True:
            try:
                message = message_queue.get(True, 0.1)
            except:
                continue
            else:
                if message["type"] == "start":
                    task_thread = threading.Thread(target=self.fetch_task, args=(task_queue,))
                    task_thread.start()
                elif message["type"] == "stop":
                    if message["data"] in self.exec_processes:
                        processes = self.exec_processes[message["data"]]
                        for process in processes:
                            if process.is_alive():
                                process.terminate()
                        del self.exec_processes[message["data"]]
                        DebugLogger("引擎终止任务成功 任务id: %s" % message["data"])
                elif message["type"] == "stopAll":
                    for task_id, processes in self.exec_processes.items():
                        for process in processes:
                            if process.is_alive():
                                process.terminate()
                        DebugLogger("引擎终止任务成功 任务id: %s" % task_id)
                    self.exec_processes.clear()
                else:  # completed
                    if message["data"] in self.exec_processes:
                        del self.exec_processes[message["data"]]

    @staticmethod
    def run_test(task, queue, current_exec_status):
        s = LMSetting(task)
        plan = s.task_analysis()
        s.create_thread(plan, queue, current_exec_status)

    @staticmethod
    def push_result(message_queue, case_result_queue):
        report = LMReport(message_queue, case_result_queue)
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
