# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: settings.py
    Time: 2021/3/24 上午9:34
-------------------------------------------------
    Change Activity: 2021/3/24 上午9:34
-------------------------------------------------
    Desc: 
"""
import json
from importlib import import_module

from magical.sync_spider.config import default_settings


class Attribute(object):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "<Attribute value=%s>" % self.value

    __repr__ = __str__


class Settings(object):

    def __init__(self, ):
        self.attrs = {}
        self.load_config(default_settings)

    def __getitem__(self, key):
        return self.attrs[key].value if key in self.attrs else None

    def load_config(self, module):
        if isinstance(module, str):
            module = import_module(module)

        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def set(self, key: str, value):
        self.attrs[key] = Attribute(value)

    def set_dict(self, values):
        for key, value in values.items():
            self.set(key, value)

    def get(self, key, default=None):
        return self[key] or default

    def get_int(self, key, default=0):
        return int(self.get(key, default))

    def get_float(self, key, default=0.0):
        return float(self.get(key, default))

    def get_list(self, key, default=None):
        value = self.get(key, default or None)
        if isinstance(value, str):
            value = value.split(",")
        return value

    def get_dict(self, key, default=None):
        value = self.get(key, default or None)
        if isinstance(value, str):
            value = json.loads(value)
        return value
