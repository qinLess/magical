# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: handler.py
    Time: 2021/5/17 下午6:07
-------------------------------------------------
    Change Activity: 2021/5/17 下午6:07
-------------------------------------------------
    Desc: 
"""
from magical.utils import load_objects


class PipelineHandler(object):

    def __init__(self, spider, **kwargs):
        self.spider = spider
        self.kwargs = kwargs
        self.logger = spider.logger
        self.settings = spider.settings

        handler_manager_cls = self.settings['PIPELINE_MIDDLEWARE_MANAGER_PATH']
        self.middleware = load_objects(handler_manager_cls)(spider)

    def pipeline(self, item, **kwargs):
        return self.middleware.pipeline(item, **kwargs)
