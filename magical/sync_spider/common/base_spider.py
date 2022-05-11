# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: base_spider.py
    Time: 2021/4/11 下午9:06
-------------------------------------------------
    Change Activity: 2021/4/11 下午9:06
-------------------------------------------------
    Desc: 
"""


class BaseSpider(object):

    def __init__(self, spider):
        self.red = spider.red
        self.logger = spider.logger
        self.post_gre = spider.post_gre
        self.download = spider.download
        self.settings = spider.settings
        self.spider_util = spider.spider_util
        self.spider_data = spider.spider_data
