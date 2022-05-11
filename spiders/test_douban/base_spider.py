# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: base_spider.py
    Time: 2021/13/13 11:30:06
-------------------------------------------------
    Change Activity: 2021/13/13 11:30:06
-------------------------------------------------
    Desc:
"""

from magical.sync_spider.common.base_spider import BaseSpider


class DoubanSpiderBaseSpider(BaseSpider):
    def __init__(self, spider):
        super().__init__(spider)
