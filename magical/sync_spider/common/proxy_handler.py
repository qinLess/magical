# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: proxy_handler.py
    Time: 2021/5/5 下午2:48
-------------------------------------------------
    Change Activity: 2021/5/5 下午2:48
-------------------------------------------------
    Desc: 
"""
import random


class ProxyHandler(object):
    __instance = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance.get(cls.__name__):
            cls.__instance[cls.__name__] = super().__new__(cls)
        return cls.__instance[cls.__name__]

    def __init__(self, spider):
        self.spider = spider
        self.logger = spider.logger

        self.proxy_list = []

        self.proxy_num = spider.settings.get('PROXY_NUM', 1)


class GetRedisProxy(ProxyHandler):
    def __init__(self, spider):
        super().__init__(spider)

    def generate_proxy(self, num):
        red_proxy = self.spider.red_proxy
        proxy_keys = list(red_proxy.keys('ip_pool_win7*'))

        for i in range(num):
            proxy = (red_proxy.get(random.choice(proxy_keys))).split("_")[0]

            new_proxy = {
                'https': f'socks5://{proxy}/',
                'http': f'socks5://{proxy}/'
            }

            if self.spider.test_ip(new_proxy):
                self.proxy_list.append(new_proxy)

    def proxy_handler(self, request=None, num=None):
        if not request:
            self.generate_proxy(num or self.proxy_num)

        else:
            if request.meta.get('proxy') in self.proxy_list:
                self.proxy_list.remove(request.meta.get('proxy'))
            self.generate_proxy(num or self.proxy_num)

    def get_proxy(self):
        return random.choice(self.proxy_list) if len(self.proxy_list) > 0 else None
