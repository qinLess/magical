# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: response.py
    Time: 2021/4/10 下午10:28
-------------------------------------------------
    Change Activity: 2021/4/10 下午10:28
-------------------------------------------------
    Desc: 
"""
import re
from lxml import etree


class Response(object):
    def __init__(self, response, request):
        self.response = response
        self.request = request

        self.meta = request.meta
        self.url = response.url
        self.status = response.status_code
        self.text = response.text
        self.headers = response.headers
        self.cookies = response.cookies

    def set_encoding(self, encoding):
        self.response.encoding = encoding
        self.text = self.response.text

    def json(self):
        try:
            return self.response.json()
        except Exception as e:
            return None

    def __str__(self):
        return "<Response: %d %s>" % (self.status, self.url)

    __repr__ = __str__

    @property
    def re(self):
        return Regex(self.text)

    @property
    def selector(self):
        selector = etree.HTML(self.text)
        return selector

    def css(self, css_select: str):
        return self.selector.cssselect(css_select)

    def xpath(self, xpath_str: str) -> list:
        result_list = self.selector.xpath(xpath_str)
        return result_list


class Regex(object):
    def __init__(self, html):
        self.html = html

    def findall(self, pattern, flags=0):
        return re.findall(pattern, self.html, flags)

    def search(self, pattern, flags=0):
        return re.search(pattern, self.html, flags)

    def match(self, pattern, flags=0):
        return re.match(pattern, self.html, flags)

    def sub(self, pattern, repl, count, flags=0):
        return re.sub(pattern, repl, self.html, count, flags)
