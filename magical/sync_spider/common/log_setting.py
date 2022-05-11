# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: log_setting.py
    Time: 2021/4/10 下午1:05
-------------------------------------------------
    Change Activity: 2021/4/10 下午1:05
-------------------------------------------------
    Desc: 
"""
import logging.config

import os
import datetime
import logging
import logging.handlers


class Logger(object):
    instance = {}
    init_flag = {}

    def __new__(cls, *args, **kwargs):
        spider = kwargs['spider']
        name = spider.name

        if not cls.instance.get(name):
            cls.instance[name] = super().__new__(cls)

        return cls.instance[name]

    def __init__(self, spider):
        name = spider.name
        if Logger.init_flag.get(name):
            return
        Logger.init_flag[name] = True

        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            day_date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_path = spider.settings['LOGGER_PATH']
            self.log_path = os.path.join(log_path or 'logs/', f'{day_date}/')
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)

            self.log_name = f'{self.log_path}{name + ".log"}'
            fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
            fh.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '[%(asctime)s] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            fh.close()
            ch.close()


def get_logger(spider):
    return Logger(spider=spider).logger
