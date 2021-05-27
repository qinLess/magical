# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: downloader.py
    Time: 2021/4/11 上午12:41
-------------------------------------------------
    Change Activity: 2021/4/11 上午12:41
-------------------------------------------------
    Desc: 
"""


class DownloaderMiddleware(object):
    __instance = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, spider, **kwargs):
        self.spider = spider
        self.proxy = spider.proxy
        self.logger = spider.logger
        self.settings = spider.settings
        self.duplicate = spider.duplicate
        self.max_retry_count = spider.settings.get_int("RETRY_COUNT")
        self.retry_status_codes = spider.settings.get_list("RETRY_STATUS_CODES")

    def process_request(self, request):
        return request

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return exception

    def _retry(self, request):
        retry_count = request.meta.get('retry_count', 0) + 1
        if retry_count < self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            return retry_request
