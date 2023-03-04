import os
from faker import Faker
from importlib import import_module, reload
import sys
from faker.providers import BaseProvider
from tools.funclib.params_enum import PARAMS_ENUM


class CustomFaker(Faker):
    def __init__(self, package='provider', lm_func=None, temp=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if lm_func is None:
            lm_func = []
        self.package = package
        self.lm_func = lm_func
        self.temp = temp
        self.func_param = PARAMS_ENUM
        self._load_module()

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
                    if value.__name__ == "LiuMaProvider":
                        self._load_lm_func(value)
                    self.add_provider(value)

    def _load_lm_func(self, provider):
        for custom in self.lm_func:
            func = provider.lm_custom_func(custom["code"], custom["params"]["names"], self.temp)
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
            setattr(provider, custom["name"], func)
