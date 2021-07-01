# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: middleware.py
    Time: 2021/01/01 11:40:25
-------------------------------------------------
    Change Activity: 2021/01/01 11:40:25
-------------------------------------------------
    Desc:
"""
import random
import time

import requests

from magical.sync_spider.extends_module.base_module.downloader import DownloaderMiddleware


# ------------------------------------------------default middleware------------------------------------------------


class HeadersMiddleware(DownloaderMiddleware):
    """请求头处理中间件"""

    def __init__(self, spider):
        super().__init__(spider)

    def process_request(self, request):
        request.headers.update({'Connection': 'close'})
        return request


class ProxyMiddleware(DownloaderMiddleware):
    """代理IP中间件"""

    def __init__(self, spider):
        super().__init__(spider)

        self.proxy.proxy_handler(num=1)

    def process_request(self, request):
        request.meta['proxy'] = self.proxy.get_proxy()
        return request

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        self.logger.error(f'ProxyMiddleware.process_exception: {exception}, request: {request}', exc_info=True)

        if isinstance(
            exception,
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
            )
        ):
            self.logger.error(f'ProxyMiddleware - 请求异常重试 - request: {request}')
            time.sleep(random.randint(3, 5))
            self.proxy.proxy_handler(request, num=1)
            return self._retry(request)

        return exception


class RequestErrorMiddleware(DownloaderMiddleware):
    """请求异常中间件"""

    def __init__(self, spider):
        super().__init__(spider)

    def process_exception(self, request, exception):
        self.logger.error(f'RequestErrorMiddleware.process_exception: {exception}, request: {request}', exc_info=True)

        if isinstance(
                exception,
                (
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ConnectTimeout,
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.Timeout,
                )
        ):
            self.logger.error(f'RequestErrorMiddleware - 请求异常重试 - request: {request}')
            time.sleep(random.randint(3, 5))
            return self._retry(request)

        elif isinstance(exception, requests.exceptions.HTTPError):
            self.logger.error(f'RequestErrorMiddleware - requests.exceptions.HTTPError - request: {request}')
            return None

        elif isinstance(exception, requests.exceptions.ChunkedEncodingError):
            self.logger.error(f'RequestErrorMiddleware - requests.exceptions.ChunkedEncodingError - request: {request}')
            return None

        elif isinstance(exception, requests.exceptions.SSLError):
            self.logger.error(f'RequestErrorMiddleware - requests.exceptions.SSLError - request: {request}')
            return None

        return exception


# -------------------------------------------------spider middleware-------------------------------------------------


class TestExcelMiddleware(DownloaderMiddleware):

    def __init__(self, spider):
        super().__init__(spider)

    def process_request(self, request):
        return request

    def process_response(self, request, response):
        if not request.use_middleware:
            return response

        return response

    def process_exception(self, request, exception):
        self.logger.error(f'TestExcelMiddleware.process_exception: {exception}, request: {request}')
        return exception
