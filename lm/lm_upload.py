# -*- coding: utf-8 -*-
import os
import threading
from lm.lm_api import LMApi


class LMUpload(object):

    def __init__(self, files, log_path):
        self.files = files
        self.log_path = log_path
        self.api = LMApi()

    def set_upload(self, task_image_path):
        threads = []
        for file in self.files:
            if file.endswith(".png"):
                uuid = file[:-4]
                thread = threading.Thread(target=self.upload, args=(task_image_path, uuid, file))
                threads.append(thread)
            else:
                os.remove(os.path.join(task_image_path, file))
        else:
            for t in threads:
                t.start()
            for t in threads:
                t.join()

    def upload(self, task_image_path, uuid, file):
        try:
            self.api.upload_screen_shot(task_image_path, uuid, self.log_path)
            os.remove(os.path.join(task_image_path, file))
        except:
            pass

