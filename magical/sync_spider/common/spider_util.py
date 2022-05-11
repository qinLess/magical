# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: spider_util.py
    Time: 2021/4/11 下午9:35
-------------------------------------------------
    Change Activity: 2021/4/11 下午9:35
-------------------------------------------------
    Desc: 
"""
import os
import json
import random
import time
import datetime
import hashlib


class SpiderUtil(object):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_agent.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        usa = json.load(f)

    def __init__(self, spider):
        self.spider = spider

    @staticmethod
    def random_ua():
        return random.choice(SpiderUtil.usa)

    @staticmethod
    def microsecond_handler(time_str, symbol='-'):
        new_time_str = time_str.replace('T', ' ')

        dt = datetime.datetime.strptime(new_time_str, "%Y-%m-%d %H:%M:%S.%f+0800")
        dt1 = time.mktime(dt.timetuple()) + (dt.microsecond / 1000000)
        dt1 = dt1 * 1000
        dt1 = dt1 - 1 if '-' == symbol else dt1 + 1
        dt2 = datetime.datetime.fromtimestamp((int(dt1)) / 1000)

        return (dt2.strftime("%Y-%m-%dT%H:%M:%S.%f+0800")).replace('000', '')

    @staticmethod
    def get_sha1_encrypt(string):
        return hashlib.sha1(string.encode()).hexdigest()

    @staticmethod
    def get_md5_encrypt(string):
        new_md5 = hashlib.md5()
        new_md5.update(string.encode(encoding='utf-8'))
        return new_md5.hexdigest()


if __name__ == '__main__':
    print(SpiderUtil.random_ua())
