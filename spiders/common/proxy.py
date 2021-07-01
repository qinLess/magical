# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: proxy.py
    Time: 2021/7/1 上午11:39
-------------------------------------------------
    Change Activity: 2021/7/1 上午11:39
-------------------------------------------------
    Desc: 
"""


class GetProxy(object):

    # spider 是爬虫实例对象
    def __init__(self, spider):
        self.logger = spider.logger

    def get_proxy(self):
        self.logger.info('获取一条代理Ip')
        return None
