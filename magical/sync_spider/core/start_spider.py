# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: start_spider.py
    Time: 2021/4/14 下午5:21
-------------------------------------------------
    Change Activity: 2021/4/14 下午5:21
-------------------------------------------------
    Desc: 
"""
from magical.sync_spider.core.spider import ThreadSyncSpider


def run_spider(spider_cls, *args, **kwargs):
    spider = spider_cls(*args, **kwargs)
    spider.start()


def run_thread_spider(items, spider_cls, *args, **kwargs):
    ThreadSyncSpider(items, spider_cls, *args, **kwargs).start()
