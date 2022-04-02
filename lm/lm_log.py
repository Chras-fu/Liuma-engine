# -*- coding: utf-8 -*-
import os
import logging
import threading
from lm.lm_config import LOG_PATH


class LMLogger(object):

    def __init__(self, logger_name='Auto Test'):
        self.logger = logging.getLogger(logger_name)
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)-4s - %(message)s")
        self.logger.setLevel(logging.INFO)

    def get_handler(self, file_path):
        p, f = os.path.split(file_path)
        if not (os.path.exists(p)):
            os.makedirs(p)
        file_handler = logging.FileHandler(file_path, encoding="utf8")
        file_handler.setFormatter(self.formatter)
        return file_handler


my_logger = LMLogger()
default_log_path = os.path.join(LOG_PATH, "engine_run.log")
my_lock = threading.RLock()


def DebugLogger(log_info, file_path=default_log_path):
    try:
        if my_lock.acquire():
            file_handler = my_logger.get_handler(file_path)
            my_logger.logger.addHandler(file_handler)
            my_logger.logger.info(log_info)
            my_logger.logger.removeHandler(file_handler)

            my_lock.release()
    except Exception as e:
        print("Failed to record debug log. Reason:\n %s" % str(e))


def ErrorLogger(log_info, file_path=default_log_path):
    try:
        if my_lock.acquire():
            file_handler = my_logger.get_handler(file_path)
            my_logger.logger.addHandler(file_handler)
            my_logger.logger.error(log_info)
            my_logger.logger.removeHandler(file_handler)

            my_lock.release()
    except Exception as e:
        print("Failed to record error log. Reason:\n %s" % str(e))
