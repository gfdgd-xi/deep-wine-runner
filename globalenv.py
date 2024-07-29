# -*- coding: utf-8 -*-

# 用于实现主模块的变量可被子模块调用和读取
# 要在主模块和需要的子模块分别 import globalenv
# 然后需要在主模块进行初始化（_init），子模块不要重复 init
# 接着即可调用 set_value 和 get_value 存放/读取变量
def _init():  #初始化（在主模块初始化，不要在子模块重复 init）
    global _global_dict
    _global_dict = {}

def set_value(key :str, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value

""" 获得一个全局变量,不存在则返回默认值 """
def get_value(key, defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue