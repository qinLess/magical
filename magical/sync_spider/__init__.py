# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: __init__.py.tmpl.py
    Time: 2021/4/10 下午4:48
-------------------------------------------------
    Change Activity: 2021/4/10 下午4:48
-------------------------------------------------
    Desc: 
"""

from magical.utils import load_objects
from magical.sync_spider.core.start_spider import run_spider, run_thread_spider
from magical.sync_spider.http.request import Request
from magical.sync_spider.core.spider import SyncSpider, ThreadSyncSpider, RedisMessageMQSpider, RabbitMessageMQSpider
from magical.sync_spider.common.log_setting import get_logger


def get_settings(settings_path=None):
    import importlib
    from magical.sync_spider.config.settings import Settings

    settings = Settings()

    if settings_path:
        custom_settings = importlib.import_module(settings_path)
        settings.load_config(custom_settings)

    return settings


class TestSyncSpider(object):
    name = 'test_sync_spider'

    def __init__(self, settings_path=None):
        self.settings = get_settings(settings_path)
        self.loop = None
        self.logger = get_logger(self)
