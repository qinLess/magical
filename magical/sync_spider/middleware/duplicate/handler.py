# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: handler.py
    Time: 2021/5/13 下午1:45
-------------------------------------------------
    Change Activity: 2021/5/13 下午1:45
-------------------------------------------------
    Desc: 
"""
import copy

from magical.utils import load_objects


class DuplicateHandler(object):

    def __init__(self, spider):
        self.spider = spider

        self.use_md5 = self.spider.settings['FILTER_USE_MD5']
        self.filter_method = load_objects(self.spider.settings['FILTER_METHOD_MANAGER'])(spider)

    def __deal_data(self, filter_data):
        if self.use_md5:
            value = self.spider.spider_util.get_md5_encrypt(filter_data)

        else:
            value = copy.deepcopy(filter_data)

        return value

    def get(self, key, value):
        return self.filter_method.get(key, self.__deal_data(value))

    def add(self, key, value):
        return self.filter_method.add(key, self.__deal_data(value))
