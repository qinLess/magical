# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: base_spider.py
    Time: 2021/01/01 11:40:25
-------------------------------------------------
    Change Activity: 2021/01/01 11:40:25
-------------------------------------------------
    Desc:
"""

from magical.sync_spider.common.base_spider import BaseSpider


class TestExcelBaseSpider(BaseSpider):
    def __init__(self, spider):
        super().__init__(spider)
