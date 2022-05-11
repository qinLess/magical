# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: settings.py
    Time: 2021/7/1 上午11:39
-------------------------------------------------
    Change Activity: 2021/7/1 上午11:39
-------------------------------------------------
    Desc: 
"""
# 统一初始化，爬虫其他工具类，模块
SPIDER_INIT_HANDLER = 'spiders.common.spider_init.SpiderInit'

EXCEL = 'spiders.common.excel'
PROXY_HANDLER = 'spiders.common.proxy.GetProxy'

REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': '6379',
    'db': '0',
    'decode_responses': True
}

