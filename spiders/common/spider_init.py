# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: spider_init.py
    Time: 2021/7/31 下午5:07
-------------------------------------------------
    Change Activity: 2021/7/31 下午5:07
-------------------------------------------------
    Desc: 
"""
from magical.sync_spider import load_files


class SpiderInit(object):
    def __init__(self, spider):
        self.settings = spider.settings

        spider.excel = load_files(self.settings['EXCEL'])
