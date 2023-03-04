import os
from functools import reduce
from faker.providers import BaseProvider
import time
from lm.lm_api import LMApi
from pypinyin import lazy_pinyin
import base64
import datetime
import json
from dateutil.relativedelta import relativedelta
from lm.lm_config import FILE_PATH


class LiuMaProvider(BaseProvider):

    @staticmethod
    def lm_custom_func(code, params, temp=None):
        def func(self, *args):
            def sys_return(res):
                names["_exec_result"] = res

            def sys_get(name):
                if name in names["_test_params"]:
                    return names["_test_params"][name]
                return names["_test_context"][name]

            def sys_put(name, val, ps=False):
                if ps:
                    names["_test_params"][name] = val
                names["_test_context"][name] = val

            names = locals()
            names["_test_context"] = temp["context"]
            names["_test_params"] = temp["params"]
            for index, value in enumerate(params):
                names[value] = args[index]
            exec(code)
            return names["_exec_result"]
        return func

    def loadfile(self, uuid):
        try:
            res = LMApi().download_test_file(uuid)
        except:
            raise Exception("拉取测试文件失败")
        else:
            return res.content

    def savefile(self, uuid):
        try:
            res = LMApi().download_test_file(uuid)
        except:
            raise Exception("拉取测试文件失败")
        else:
            file_name = res.headers.get("Content-Disposition").split("=")[1][1:-1]
            dir_path = os.path.join(FILE_PATH, uuid)
            file_path = os.path.join(dir_path, file_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                with open(file_path, 'wb+') as f:
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                f.close()
            return file_path

    def b64encode_str(self, s: str):
        return base64.b64encode(s.encode('utf-8')).decode()

    def b64encode_bytes(self, s: bytes):
        return base64.b64encode(s).decode()

    def b64encode_file(self, uuid):
        content = self.loadfile(uuid)
        return base64.b64encode(content).decode()

    def b64decode_toStr(self, s: str):
        return base64.b64decode(s).decode()

    def b64decode_toBytes(self, s: str):
        return base64.b64decode(s)

    def arithmetic(self, expression: str):
        try:
            return eval(expression)
        except Exception:
            raise Exception("四则运算表达式错误:%s" % expression)

    def current_time(self, s: str = '%Y-%m-%d'):
        if s.lower() == "none":
            return int(time.time() * 1000)
        return time.strftime(s)

    def year_shift(self, shift, s: str = '%Y-%m-%d'):
        now_date = datetime.datetime.now()
        shift_date = now_date + relativedelta(years=shift)
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def month_shift(self, shift, s: str = '%Y-%m-%d'):
        now_date = datetime.datetime.now()
        shift_date = now_date + relativedelta(months=shift)
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def week_shift(self, shift, s: str = '%Y-%m-%d'):
        now_date = datetime.datetime.now()
        delta = datetime.timedelta(weeks=shift)
        shift_date = now_date + delta
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def date_shift(self, shift, s: str = '%Y-%m-%d'):
        now_date = datetime.datetime.now()
        delta = datetime.timedelta(days=shift)
        shift_date = now_date + delta
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def hour_shift(self, shift, s: str = '%Y-%m-%d %H:%M:%S'):
        now_date = datetime.datetime.now()
        delta = datetime.timedelta(hours=shift)
        shift_date = now_date + delta
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def minute_shift(self, shift, s: str = '%Y-%m-%d %H:%M:%S'):
        now_date = datetime.datetime.now()
        delta = datetime.timedelta(minutes=shift)
        shift_date = now_date + delta
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def second_shift(self, shift, s: str = '%Y-%m-%d %H:%M:%S'):
        now_date = datetime.datetime.now()
        delta = datetime.timedelta(seconds=shift)
        shift_date = now_date + delta
        if s.lower() == "none":
            return int(shift_date.timestamp() * 1000)
        return shift_date.strftime(s)

    def lenof(self, array):
        return len(array)

    def indexof(self, array, index):
        return array[index]

    def keyof(self, map, key):
        return map[key]

    def pinyin(self, cname: str):
        return reduce(lambda x, y: x + y, lazy_pinyin(cname))

    def substing(self, s, start: int=0, end: int=-1):
        return s[start:end]

    def extract(self, data):
        return data

    def replace(self, s, old, new):
        return s.replace(old, new)

    def map_dumps(self, tar):
        return json.dumps(tar)

    def array_dumps(self, tar):
        return json.dumps(tar)
