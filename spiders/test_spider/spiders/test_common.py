# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: test_common.py
    Time: 2021/31/31 17:34:58
-------------------------------------------------
    Change Activity: 2021/31/31 17:34:58
-------------------------------------------------
    Desc:
"""
import os
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(file_path)

from magical.sync_spider import SyncSpider, run_spider


class TestCommonSpider(SyncSpider):
    name = 'test_common'
    settings_path = 'spiders.test_spider.settings'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        custom_setting = {}
        kwargs.update(dict(custom_setting=custom_setting))
        super().__init__(*args, **kwargs)

    def start_spider(self):
        print(self.excel)


if __name__ == '__main__':
    run_spider(TestCommonSpider)
