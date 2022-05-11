# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: handler.py
    Time: 2021/4/18 下午12:37
-------------------------------------------------
    Change Activity: 2021/4/18 下午12:37
-------------------------------------------------
    Desc: 
"""
import urllib3
import cfscrape
import requests
from urllib.parse import urlparse
from requests import adapters

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
adapters.DEFAULT_RETRIES = 5

from magical.sync_spider.http.response import Response


class DownloadHandler(object):
    """请求中间件处理"""

    def __init__(self, spider, **kwargs):
        self.spider = spider
        self.kwargs = kwargs
        self.logger = spider.logger
        self.settings = spider.settings

        self.session = requests.session()
        self.scrape = cfscrape.create_scraper(delay=self.settings['SCRAPER_DELAY'])
        self.scrape_session = cfscrape.create_scraper(sess=self.session, delay=self.settings['SCRAPER_DELAY'])

    def fetch(self, request):
        """开始下载

        Args:
            request: request 对象
        Returns:
            response 对象
        """

        if request.s5:
            instance = self.scrape
            if request.session:
                instance = self.scrape_session

        elif request.session:
            instance = self.session

        else:
            instance = requests

        if request.method == 'POST':
            response = instance.post(
                request.url,
                data=request.data,
                json=request.json,
                headers=request.headers,
                params=request.params,
                proxies=request.meta.get('proxy'),
                verify=self.settings['REQUEST_VERIFY'],
                timeout=self.settings['REQUEST_TIMEOUT'],
                **request.kwargs
            )
        else:
            response = instance.get(
                request.url,
                headers=request.headers,
                params=request.params,
                proxies=request.meta.get('proxy'),
                verify=self.settings['REQUEST_VERIFY'],
                timeout=self.settings['REQUEST_TIMEOUT'],
                **request.kwargs
            )

        response.encoding = request.encoding

        res = Response(response, request)

        self.logger.debug(f"Downloaded ({res.status}) {str(request)}")
        return res
