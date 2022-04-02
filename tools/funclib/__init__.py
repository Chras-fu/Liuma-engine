from .load_faker import CustomFaker
import time


def get_func_lib(lm_func=None):
    faker = CustomFaker(locale='zh_cn', package='provider', lm_func=lm_func)
    CustomFaker.seed(str(time.time()))
    return faker

