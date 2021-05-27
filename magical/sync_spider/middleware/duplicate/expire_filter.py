# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: expire_filter.py
    Time: 2021/5/13 下午2:26
-------------------------------------------------
    Change Activity: 2021/5/13 下午2:26
-------------------------------------------------
    Desc: 
"""
import time


class ExpireFilter(object):

    def __init__(self, spider):
        red_name = spider.settings['FILTER_REDIS_NAME']

        self.expire = spider.settings['FILTER_REDIS_KEY_EXPIRE']
        self.red = getattr(spider, red_name) if not red_name else spider.red

    @property
    def current_timestamp(self):
        return int(time.time())

    def get(self, filter_key, value):
        return self.red.zscore(filter_key, value)

    def add(self, filter_key, value):
        return self.red.zadd(filter_key, value)

    # def del_expire_key(self):
    #     self.red.zremrangebyscore(self.name, "-inf", self.current_timestamp - self.expire_time)
    #
    # def record_expire_time(self):
    #     if self.expire_time_record_key:
    #         self.red.hset(self.expire_time_record_key, key=self.name, value=self.expire_time)
