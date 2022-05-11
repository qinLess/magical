# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: manager.py
    Time: 2021/5/17 下午5:54
-------------------------------------------------
    Change Activity: 2021/5/17 下午5:54
-------------------------------------------------
    Desc: 
"""
from collections import defaultdict

from magical.sync_spider.extends_module.base_module.pipeline import PipelineMiddleware
from magical.sync_spider.common.utils import call_func_item
from magical.utils import load_objects


class PipelineMiddlewareManager(object):
    def __init__(self, spider):
        self.methods = defaultdict(list)
        self.spider = spider
        self.settings = spider.settings
        self.middleware_s = self.__load_middleware()

        for miw in self.middleware_s:
            self.__add_middleware(miw)

    def __load_middleware(self):
        middleware_s = []
        middleware_s_dict = self.settings["PIPELINE_MIDDLEWARE_PATH"]
        middleware_s_list = sorted(middleware_s_dict.items(), key=lambda x: x[1])

        for middleware_key, value in middleware_s_list:
            middleware = load_objects(middleware_key)
            if issubclass(middleware, PipelineMiddleware):
                middleware_instance = middleware(self.spider)
                middleware_s.append(middleware_instance)
        return middleware_s

    def __add_middleware(self, miw):
        if hasattr(miw, "process_item"):
            self.methods['process_item'].append(miw.process_item)

        if hasattr(miw, "process_exception"):
            self.methods['process_exception'].append(miw.process_exception)

    def pipeline(self, item, **kwargs):

        def process_item(item):
            for method in self.methods['process_item']:
                item = method(item, **kwargs)
                if not isinstance(item, type(item)):
                    return item

            return item

        def process_exception(exception):
            for method in self.methods['process_exception']:
                exception = method(item, exception)
                if not exception:
                    return exception
            return exception

        return call_func_item(process_item, process_exception, item)
