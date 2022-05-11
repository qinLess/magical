# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: manager.py
    Time: 2021/4/18 下午12:37
-------------------------------------------------
    Change Activity: 2021/4/18 下午12:37
-------------------------------------------------
    Desc: 
"""
from collections import defaultdict

from magical.sync_spider.extends_module.base_module.downloader import DownloaderMiddleware
from magical.sync_spider.http.request import Request
from magical.sync_spider.common.utils import call_func
from magical.utils import load_objects


class DownloadMiddlewareManager(object):
    def __init__(self, spider):
        self.methods = defaultdict(list)
        self.spider = spider
        self.settings = spider.settings
        self.middleware_s = self._load_middleware()

        for miw in self.middleware_s:
            self._add_middleware(miw)

    def _load_middleware(self):
        middleware_s = []
        middleware_s_dict = self.settings["DOWNLOAD_MIDDLEWARE_PATH"]
        middleware_s_list = sorted(middleware_s_dict.items(), key=lambda x: x[1])

        for middleware_key, value in middleware_s_list:
            middleware = load_objects(middleware_key)
            if issubclass(middleware, DownloaderMiddleware):
                middleware_instance = middleware(self.spider)
                middleware_s.append(middleware_instance)
        return middleware_s

    def _add_middleware(self, miw):
        if hasattr(miw, "process_request"):
            self.methods['process_request'].append(miw.process_request)

        if hasattr(miw, "process_response"):
            self.methods['process_response'].append(miw.process_response)

        if hasattr(miw, "process_exception"):
            self.methods['process_exception'].append(miw.process_exception)

    def download(self, download_func, request):
        this = self

        def process_request(request):
            for method in this.methods['process_request']:
                request = method(request)
                if not request:
                    return request
            response = download_func(request)
            return response

        def process_response(response):
            for method in this.methods['process_response']:
                response = method(request, response)
                if isinstance(response, Request) or not response:
                    return response
            return response

        def process_exception(exception):
            for method in this.methods['process_exception']:
                response = method(request, exception)
                if isinstance(response, Request) or not response:
                    return response
            return exception

        resp = call_func(process_request, process_exception, process_response, request)

        return resp
