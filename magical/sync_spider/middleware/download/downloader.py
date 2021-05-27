# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: downloader.py
    Time: 2021/4/10 下午11:27
-------------------------------------------------
    Change Activity: 2021/4/10 下午11:27
-------------------------------------------------
    Desc: 
"""
from magical.utils import load_objects


class Downloader(object):
    """Downloader中间件"""

    def __init__(self, spider):
        handler_cls = spider.settings['DOWNLOAD_HANDLER_PATH']
        handler_manager_cls = spider.settings['DOWNLOAD_MIDDLEWARE_MANAGER_PATH']
        self.handler = load_objects(handler_cls)(spider)
        self.middleware = load_objects(handler_manager_cls)(spider)

    def _download(self, request):
        """请求函数
        Args:
            request: request对象
        Returns:
            response 对象
        """
        resp = self.handler.fetch(request)
        return resp

    def fetch(self, request):
        """请求函数
        Args:
            request: request对象
        Returns:
            response 对象
        """
        resp = self.middleware.download(self._download, request)
        return resp
