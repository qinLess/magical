# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: goods_utils.py
    Time: 2021/4/20 上午12:31
-------------------------------------------------
    Change Activity: 2021/4/20 上午12:31
-------------------------------------------------
    Desc: 
"""
import os
import time
import datetime

from importlib import import_module
from decimal import Decimal, ROUND_HALF_UP


def log_path(project_path):
    """获取 logs 路径

    Args:
        project_path: 项目绝对路径
    Returns: 返回 log 路径
    """
    s_path = os.path.basename(os.path.abspath(project_path))

    if s_path == 'spiders':
        return os.path.join(os.path.dirname(project_path), 'logs')

    else:
        return log_path(os.path.dirname(project_path))


# 加载 py 文件
def load_files(path):
    return import_module(path)


# 加载模块类函数
def load_objects(path):
    try:
        dot = path.rindex('.')
    except ValueError as e:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def round_half_up(digit, n=2):
    return Decimal(str(digit)).quantize(Decimal('0.' + '0' * n), rounding=ROUND_HALF_UP)


def get_fmt_time(fmt="%Y-%m-%d %H:%M:%S", timestamp=None):
    if timestamp:
        return time.strftime(fmt, time.localtime(int(timestamp)))
    return datetime.datetime.now().strftime(fmt)
