# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: utils.py
    Time: 2021/4/10 下午9:36
-------------------------------------------------
    Change Activity: 2021/4/10 下午9:36
-------------------------------------------------
    Desc: 
"""
import time

from magical.utils import round_half_up, get_fmt_time

start_time = time.time()
success_rate = 0
success_num = 0
failure_num = 0
end_time = None
req_num = None


def _gen_content(name):
    global req_num, success_rate
    req_num = success_num + failure_num

    success_rate = float(round_half_up(success_num / req_num, 4)) * 100 if req_num else 0

    return [
        f'爬虫名称: {name}',
        f'请求成功率: {success_rate}%',
        f'请求成功次数: {success_num}',
        f'请求失败次数: {failure_num}',
        f'开始时间: {get_fmt_time(timestamp=start_time)}',
        f'结束时间: {get_fmt_time(timestamp=end_time)}',
    ]


def call_func(request_func, exception_func, response_func, *args, **kwargs):
    global success_num, failure_num, end_time

    failure_num += 1
    try:
        result = request_func(*args, **kwargs)

    except Exception as exc:
        failure_num -= 1
        return exception_func(exc)

    else:
        failure_num -= 1
        success_num += 1
        return response_func(result)

    finally:
        end_time = time.time()


def call_func_item(item_func, exception_func, *args, **kwargs):
    try:
        return item_func(*args, **kwargs)

    except Exception as exc:
        return exception_func(exc)
