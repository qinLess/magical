# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: pipeline.py
    Time: 2021/5/17 下午5:56
-------------------------------------------------
    Change Activity: 2021/5/17 下午5:56
-------------------------------------------------
    Desc: 
"""


class PipelineMiddleware(object):
    __instance = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, spider, **kwargs):
        self.spider = spider
        self.logger = spider.logger
        self.settings = spider.settings

    def process_item(self, item, **kwargs):
        """数据处理

        Args:
            item  : 要处理的数据
            kwargs:
                table_name: 表名称
                replace   : True or False (mysql 数据库使用)
                ignore    : True or False (mysql 数据库使用)
                indexes   : 数据库表唯一索引字段 (PostGreSql 数据库使用)

        Return:
            返回的数据类型如果不等于 type(item) 则不会调用后面的 pipeline process_item 函数
        """
        return item

    def process_exception(self, item, exception, **kwargs):
        return exception
