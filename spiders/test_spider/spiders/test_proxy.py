# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: test_proxy.py
    Time: 2021/01/01 11:40:08
-------------------------------------------------
    Change Activity: 2021/01/01 11:40:08
-------------------------------------------------
    Desc:
"""
import os
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(file_path)

from magical.sync_spider import SyncSpider, Request, run_spider


class TestProxySpider(SyncSpider):
    name = 'test_proxy'
    settings_path = 'spiders.test_spider.settings'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        custom_setting = {}
        kwargs.update(dict(custom_setting=custom_setting))
        super().__init__(*args, **kwargs)

    def start_spider(self):
        print(self.proxy.get_proxy())

        self.download(
            url='',
            params={},
            method='POST',
            data={},
            headers={},
            meta={
                'proxy': self.proxy.get_proxy()
            }
        )

        request = Request(
            url='',
            params={},
            method='POST',
            data={},
            headers={},
            meta={
                'proxy': self.proxy.get_proxy()
            }
        )
        self.download(request)


if __name__ == '__main__':
    run_spider(TestProxySpider)
