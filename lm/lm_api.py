# -*- coding: utf-8 -*-
import base64
import requests
import time
from lm.lm_config import *
from lm.lm_log import DebugLogger, ErrorLogger
from tools.utils import utils


class Api(object):

    def __init__(self):
        config = LMConfig()
        self.url = config.url[:-1] if config.url.endswith("/") else config.url
        self.engine = config.engine
        self.secret = config.secret
        self.proxy = None
        if config.enable_proxy.lower() == "true":
            try:
                self.proxy = utils.proxies_join(config.platform_proxy)
            except:
                pass

    def request(self, url, data):
        header = self.load_header()
        response = requests.post(url=url, json=data, headers=header, proxies=self.proxy, timeout=30)
        return response

    def download(self, url):
        header = self.load_header()
        response = requests.get(url=url, headers=header, proxies=self.proxy, stream=True, timeout=30)
        return response

    @staticmethod
    def save_token(token):
        reader = IniReader()
        DebugLogger("更新token")
        reader.modify("Header", "token", token)

    @staticmethod
    def load_header():
        config = LMConfig()
        header = config.header
        return header


class LMApi(Api):

    def apply_token(self):
        """"申请token"""
        url = self.url + "/openapi/engine/token/apply"
        data = {
            "engineCode": self.engine,
            "engineSecret": self.secret,
            "timestamp": int(time.time()),
        }
        try:
            res = self.request(url=url, data=data)
            if res.status_code == 200:
                status = res.json()["status"]
                if status == 0:
                    token = res.json()["data"]
                    self.save_token(token)
                elif status == 2050:
                    DebugLogger("调用申请token接口 引擎id或秘钥错误")
                else:
                    DebugLogger("调用申请token接口 token生成失败")
            else:
                DebugLogger("调用申请token接口 响应状态为：%s" % res.status_code)
        except Exception as e:
            ErrorLogger("调用申请token接口 发生错误 错误信息为：%s" % e)

    def send_heartbeat(self, log_path):
        """"发送心跳"""
        url = self.url + "/openapi/engine/heartbeat/send"
        for index in range(2):
            data = {
                "engineCode": self.engine,
                "timestamp": int(time.time())
            }
            try:
                if index > 0:
                    DebugLogger("-------重试调用发送引擎心跳接口--------", file_path=log_path)
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        DebugLogger("发送引擎心跳成功", file_path=log_path)
                        return True
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token", file_path=log_path)
                        self.apply_token()
                        continue
                    else:
                        DebugLogger("发送引擎心跳失败", file_path=log_path)
                else:
                    DebugLogger("调用发送引擎心跳接口 响应状态为：%s" % res.status_code, file_path=log_path)
            except Exception as e:
                ErrorLogger("调用发送引擎心跳接口 发生错误 错误信息为：%s" % e, file_path=log_path)
            break

    def fetch_task(self):
        """"获取任务"""
        url = self.url + "/openapi/engine/task/fetch"
        for index in range(2):
            data = {
                "engineCode": self.engine,
                "timestamp": int(time.time())
            }
            try:
                if index > 0:
                    DebugLogger("-------重试调用获取引擎任务接口--------")
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        return res.json()["data"]
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token")
                        self.apply_token()
                        continue
                    else:
                        DebugLogger("获取引擎任务请求失败")
                else:
                    DebugLogger("调用获取引擎任务接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用获取引擎任务接口 发生错误 错误信息为：%s" % e)
            break

    def upload_result(self, task_id, data_type, result):
        """"上传执行结果"""
        url = self.url + "/openapi/engine/result/upload"
        for index in range(2):
            data = {
                "engineCode": self.engine,
                "timestamp": int(time.time()),
                "taskId": task_id,
                "caseResultList": result
            }
            try:
                if index > 0:
                    DebugLogger("-------重试调用上传执行结果接口--------")
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        return True
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token")
                        self.apply_token()
                        continue
                    else:
                        DebugLogger("上传执行结果请求失败")
                else:
                    DebugLogger("调用上传执行结果接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用上传执行结果接口 发生错误 错误信息为：%s" % e)
            break

    def complete_task(self, task_id):
        """"反馈任务结束"""
        url = self.url + "/openapi/engine/task/complete"
        for index in range(2):
            data = {
                "engineCode": self.engine,
                "timestamp": int(time.time()),
                "taskId": task_id
            }
            try:
                if index > 0:
                    DebugLogger("-------重试调用反馈任务结束接口--------")
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        return True
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token")
                        self.apply_token()
                        continue
                    else:
                        DebugLogger("反馈任务结束请求失败")
                else:
                    DebugLogger("调用反馈任务结束接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用反馈任务结束接口 发生错误 错误信息为：%s" % e)
            break

    def download_task_file(self, path):
        """下载任务文件"""
        url = self.url + path
        for index in range(2):
            try:
                if index > 0:
                    DebugLogger("-------重试调用下载任务文件接口--------")
                res = self.download(url)
                if res.status_code == 200:
                    if not isinstance(res.content, bytes):
                        status = res.json()["status"]
                        if status in (2020, 2030, 2040):
                            DebugLogger("token校验错误 重新申请token")
                            self.apply_token()
                            continue
                        else:
                            DebugLogger("下载任务文件失败")
                    else:
                        return res
                else:
                    DebugLogger("调用下载任务文件接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用下载任务文件接口 发生错误 错误信息为：%s" % e)
            break

    def download_test_file(self, uuid):
        """下载测试文件"""
        url = self.url + "/openapi/download/test/file/" + uuid
        for index in range(2):
            try:
                if index > 0:
                    DebugLogger("-------重试调用下载测试文件接口--------")
                res = self.download(url)
                if res.status_code == 200:
                    if not isinstance(res.content, bytes):
                        status = res.json()["status"]
                        if status in (2020, 2030, 2040):
                            DebugLogger("token校验错误 重新申请token")
                            self.apply_token()
                            continue
                        else:
                            DebugLogger("下载测试文件失败")
                    else:
                        return res
                else:
                    DebugLogger("调用下载测试文件接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用下载测试文件接口 发生错误 错误信息为：%s" % e)
            break

    def upload_screen_shot(self,task_image_path, uuid, log_path):
        """"上传执行截图"""
        url = self.url + "/openapi/engine/screenshot/upload"
        for index in range(2):
            data = {
                "fileName": "%s.png" % uuid,
                "engineCode": self.engine,
                "timestamp": int(time.time())
            }
            with open(os.path.join(task_image_path, "%s.png" % uuid), "rb") as f:
                file = base64.b64encode(f.read()).decode()
                data["base64String"] = file
            try:
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        DebugLogger("截图%s上传成功" % uuid, file_path=log_path)
                        return True
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token", file_path=log_path)
                        self.apply_token()
                        continue
                    else:
                        ErrorLogger("截图%s上传失败" % uuid, file_path=log_path)
                else:
                    DebugLogger("调用上传截图接口 响应状态为：%s" % res.status_code, file_path=log_path)
            except Exception as e:
                ErrorLogger("调用上传截图接口 发生错误 错误信息为：%s" % e, file_path=log_path)
            break
        else:
            ErrorLogger("截图%s上传失败" % uuid, file_path=log_path)
            return False

    def get_task_status(self, task_id):
        """"获取任务状态"""
        url = self.url + "/openapi/engine/task/status"
        for index in range(2):
            data = {
                "taskId": task_id,
                "engineCode": self.engine,
                "timestamp": int(time.time())
            }
            try:
                if index > 0:
                    DebugLogger("-------重试调用获取任务状态接口--------")
                res = self.request(url, data)
                if res.status_code == 200:
                    status = res.json()["status"]
                    if status == 0:
                        return res.json()["data"]
                    elif status in (2020, 2030, 2040):
                        DebugLogger("token校验错误 重新申请token")
                        self.apply_token()
                        continue
                    else:
                        DebugLogger("获取任务状态请求失败")
                else:
                    DebugLogger("调用获取任务状态接口 响应状态为：%s" % res.status_code)
            except Exception as e:
                ErrorLogger("调用获取任务状态接口 发生错误 错误信息为：%s" % e)
            break
        else:
            return None
