import json
import os
from ws4py.client.threadedclient import WebSocketClient
from lm.lm_config import LOG_PATH
from lm.lm_log import DebugLogger


class Client(WebSocketClient):

    def __init__(self, url, queue):
        self.queue = queue
        WebSocketClient.__init__(self, url)
        self.log_path = os.path.join(LOG_PATH, "engine_status.log")

    def opened(self):
        DebugLogger("-------------------------------------------------", file_path=self.log_path)
        DebugLogger("心跳连接成功", file_path=self.log_path)
        DebugLogger("-------------------------------------------------", file_path=self.log_path)

    def closed(self, code, reason=None):
        DebugLogger("-------------------------------------------------", file_path=self.log_path)
        DebugLogger("心跳关闭 原因%s %s" % (code, reason), file_path=self.log_path)
        DebugLogger("-------------------------------------------------", file_path=self.log_path)

    def received_message(self, resp):
        self.queue.put(json.loads(str(resp)))

