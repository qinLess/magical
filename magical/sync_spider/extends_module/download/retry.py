# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: retry.py
    Time: 2021/4/11 上午12:51
-------------------------------------------------
    Change Activity: 2021/4/11 上午12:51
-------------------------------------------------
    Desc: 
"""
from magical.sync_spider.extends_module.base_module.downloader import DownloaderMiddleware


class RetryMiddleware(DownloaderMiddleware):
    RETRY_EXCEPTIONS = ()

    def __init__(self, spider):
        super().__init__(spider)

    def process_response(self, request, response):
        if not request.use_middleware:
            return response
        if not request.meta.get("is_retry", False):
            return response
        if response.status in self.retry_status_codes:
            return self._retry(request) or response
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, self.RETRY_EXCEPTIONS) and request.meta.get("is_retry", False):
            return self._retry(request)
