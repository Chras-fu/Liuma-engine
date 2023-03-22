import os
from faker import Faker
from importlib import import_module, reload
import sys
from faker.providers import BaseProvider
from tools.funclib.params_enum import PARAMS_ENUM


class CustomFaker(Faker):
    def __init__(self, package='provider', test=None, lm_func=None, temp=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if lm_func is None:
            lm_func = []
        self.package = package
        self.test = test
        self.print = print
        self.lm_func = lm_func
        self.temp = temp
        self.func_param = PARAMS_ENUM
        self._load_module()
        self._load_lm_func()

    def __call__(self, name, *args, **kwargs):
        return getattr(self, name)(*args, **kwargs)

    def _read_module(self):
        module_path = os.path.join(os.path.dirname(__file__), self.package)
        module_list = []
        for file_name in os.listdir(module_path):
            if file_name[-2:] == "py":
                module_name = __package__ + "." + self.package + "." + file_name[0:-3]
                module_list.append(module_name)
        return module_list

    def _load_module(self):
        for name in self._read_module():
            if name not in sys.modules:
                module = import_module(name)
            else:
                module = sys.modules.get(name)
                reload(module)
            for value in module.__dict__.values():
                if type(value) is type and BaseProvider in value.__bases__:
                    self.add_provider(value)

    def _load_lm_func(self):
        for custom in self.lm_func:
            func = self._lm_custom_func(custom["code"], custom["params"]["names"], self.test, self.temp)
            params = []
            for value in custom["params"]["types"]:
                if value == "Int":
                    params.append(int)
                elif value == "Float":
                    params.append(float)
                elif value == "Boolean":
                    params.append(bool)
                elif value == "Bytes":
                    params.append(bytes)
                elif value == "JSONObject":
                    params.append(dict)
                elif value == "JSONArray":
                    params.append(list)
                elif value == "Other":
                    params.append(None)
                else:
                    params.append(str)
            self.func_param[custom["name"]] = params
            setattr(self, custom["name"], func)

    def _lm_custom_func(self, code, params, test, temp):
        def func(*args):
            def print(*args, sep=' ', end='\n', file=None, flush=False):
                if file is None or file in (sys.stdout, sys.stderr):
                    file = names["_test"].stdout_buffer
                self.print(*args, sep=sep, end=end, file=file, flush=flush)

            def sys_return(res):
                names["_exec_result"] = res

            def sys_get(name):
                if name in names["_test_context"]:
                    return names["_test_context"][name]
                elif name in names["_test_params"]:
                    return names["_test_params"][name]
                else:
                    raise KeyError("不存在的公共参数或关联变量: {}".format(name))

            def sys_put(name, val, ps=False):
                if ps:
                    names["_test_params"][name] = val
                else:
                    names["_test_context"][name] = val

            names = locals()
            names["_test_context"] = temp["context"]
            names["_test_params"] = temp["params"]
            names["_test"] = test
            for index, value in enumerate(params):
                names[value] = args[index]
            exec(code)
            return names["_exec_result"]
        return func
