import json
import re

from tools.utils.utils import proxies_join, handle_form_data, handle_files


class ApiRequestCollector:

    def __init__(self):
        self.apiId = None
        self.apiName = None
        self.method = None
        self.url = None
        self.path = None
        self.protocol = None
        self.body_type = None
        self.others = {}
        self.controller = {}
        self.looper = {}
        self.conditions = []
        self.assertions = []
        self.relations = []

    def collect_flag(self, api_data, arg_name):
        if arg_name not in api_data or api_data[arg_name] is None:
            raise NotExistedFieldError('接口数据{}字段不存在或为空'.format(arg_name))
        elif type(api_data[arg_name]) is str and len(api_data[arg_name]) == 0:
            raise NotExistedFieldError('接口数据{}字段长度为0'.format(arg_name))
        else:
            setattr(self, arg_name, api_data[arg_name])

    def collect_other(self, api_data, arg_name, func=lambda x: x):
        if arg_name not in api_data or api_data[arg_name] is None or len(api_data[arg_name]) == 0:
            self.others[arg_name] = None
        else:
            self.others[arg_name] = func(api_data[arg_name])

    def collect_context(self, api_data, arg_name):
        if arg_name not in api_data or api_data[arg_name] is None or len(api_data[arg_name]) == 0:
            setattr(self, arg_name, None)
        else:
            setattr(self, arg_name, api_data[arg_name])

    def collect_id(self, api_data):
        self.collect_flag(api_data, "apiId")

    def collect_name(self, api_data):
        self.collect_flag(api_data, "apiName")

    def collect_protocol(self, api_data):
        self.collect_flag(api_data, "protocol")

    def collect_method(self, api_data):
        if 'method' not in api_data or api_data['method'] is None or len(api_data['method']) == 0:
            raise UnDefinableMethodError("接口{}未定义请求方法".format(api_data['apiId']))
        method = api_data['method'].upper()

        self.method = method

    def collect_url(self, api_data):
        if 'url' not in api_data or api_data['url'] is None or len(api_data['url']) == 0:
            raise UnDefinablePathError("接口{}未设置域名".format(api_data['apiId']))
        else:
            self.url = api_data['url']

    def collect_path(self, api_data):
        if 'path' not in api_data or api_data['path'] is None or len(api_data['path']) == 0:
            raise UnDefinablePathError("接口{}未设置路径".format(api_data['apiId']))
        else:
            fields = re.findall(r'\{(.*?)\}', api_data['path'])
            path = api_data['path']
            for field in fields:
                result = "{%s}" % field
                if field in api_data['rest']:
                    result = api_data["rest"][field]  # 将path中的参数替换成rest
                if "#{%s}" % field in path: # 兼容老版本#{name}
                    path = path.replace("#{%s}" % field, result)
                else:
                    path = path.replace("{%s}" % field, result)
            self.path = path

    def collect_controller(self, api_data):
        if "sleepBeforeRun" not in api_data["controller"]:
            api_data["controller"]["sleepBeforeRun"] = 0  # 默认执行前不等待
        if "sleepAfterRun" not in api_data["controller"]:
            api_data["controller"]["sleepAfterRun"] = 0  # 默认执行完成不等待
        if "useSession" not in api_data["controller"]:
            api_data["controller"]["useSession"] = "false"  # 默认不使用session
        if "saveSession" not in api_data["controller"]:
            api_data["controller"]["saveSession"] = "false"  # 默认不保存session
        if "pre" not in api_data["controller"]:
            api_data["controller"]["pre"] = None  # 默认没有前置脚本和sql
        if "post" not in api_data["controller"]:
            api_data["controller"]["post"] = None  # 默认没有后置脚本和sql
        if "errorContinue" not in api_data["controller"]:
            api_data["controller"]["errorContinue"] = "false"  # 默认错误后不再执行
        self.controller = api_data["controller"]

    def collect_conditions(self, api_data):
        if "whetherExec" in api_data["controller"]:
            self.conditions = json.loads(api_data["controller"]["whetherExec"])

    def collect_looper(self, api_data):
        if "loopExec" in api_data["controller"]:
            self.looper = json.loads(api_data["controller"]["loopExec"])

    def collect_query(self, api_data):
        if len(api_data["query"]) > 0:
            self.others["params"] = api_data["query"]
        else:
            self.others["params"] = None

    def collect_headers(self, api_data):
        self.collect_other(api_data, 'headers')

    def collect_cookies(self, api_data):
        if self.others['headers'] is not None:
            pop_key = None
            for key in self.others['headers']:
                if key.strip().lower() in ['cookie', 'cookies']:
                    pop_key = key
                    break
            if pop_key is not None:
                value = self.others['headers'].pop(pop_key)
                self.others['headers']['cookie'] = value

    def collect_proxies(self, api_data):
        self.collect_other(api_data, 'proxies', proxies_join)

    def collect_body(self, api_data):
        body = api_data["body"]
        if body is None:
            return
        self.body_type = body["type"]
        if body["type"] == "json":
            if body["json"] != '':
                body_json = json.loads(body["json"])
                if len(body_json) > 0:
                    self.others["json"] = body_json
        elif body["type"] in ("form-urlencoded", "form-data"):
            body_data, body_file = handle_form_data(body["form"])
            if len(body_data) > 0:
                self.others["data"] = body_data
            if len(body_file) > 0:
                self.others["files"] = body_file
        elif body["type"] in ("text", "xml", "html"):
            if body["raw"] != "":
                self.others["data"] = body["raw"]
        elif body["type"] == "file":
            files = handle_files(body["file"])
            if len(files) > 0:
                self.others["files"] = files

    def collect_stream(self, api_data):
        if "requireStream" in api_data["controller"]:
            if api_data["controller"]["requireStream"].lower() == "true":
                self.others["stream"] = True
            else:
                self.others["stream"] = False
        else:
            self.others["stream"] = None

    def collect_verify(self, api_data):
        if "requireVerify" in api_data["controller"]:
            if api_data["controller"]["requireVerify"].lower() == "true":
                self.others["verify"] = True
            else:
                self.others["verify"] = False
        else:
            self.others["verify"] = None

    def collect_auth(self, api_data):
        pass

    def collect_timeout(self, api_data):
        if "timeout" in api_data["controller"]:
            self.others["timeout"] = int(api_data["controller"]["timeout"])
        else:
            self.others["timeout"] = None

    def collect_allow_redirects(self, api_data):
        pass

    def collect_hooks(self, api_data):
        pass

    def collect_cert(self, api_data):
        pass

    def collect_assertions(self, api_data):
        self.collect_context(api_data, 'assertions')

    def collect_relations(self, api_data):
        self.collect_context(api_data, 'relations')

    def collect(self, api_data):
        self.collect_id(api_data)
        self.collect_name(api_data)
        self.collect_method(api_data)
        self.collect_url(api_data)
        self.collect_path(api_data)

        self.collect_controller(api_data)

        self.collect_headers(api_data)
        self.collect_cookies(api_data)
        self.collect_proxies(api_data)

        self.collect_query(api_data)
        self.collect_body(api_data)

        self.collect_verify(api_data)
        self.collect_stream(api_data)
        self.collect_auth(api_data)
        self.collect_timeout(api_data)
        self.collect_allow_redirects(api_data)
        self.collect_hooks(api_data)
        self.collect_cert(api_data)

        self.collect_assertions(api_data)
        self.collect_relations(api_data)


class UnDefinableMethodError(Exception):
    """未定义请求方法"""


class UnDefinablePathError(Exception):
    """未定义请求路径"""


class NotExistedFieldError(Exception):
    """未定义必须字段"""


class NotExistedFileUploadType(Exception):
    """未定义的文件上传方式"""
