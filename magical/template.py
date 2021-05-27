# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: template.py
    Time: 2021/4/14 下午3:37
-------------------------------------------------
    Change Activity: 2021/4/14 下午3:37
-------------------------------------------------
    Desc: 
"""
import os
import re
import string


def render_template_file(path, **kwargs):
    with open(path, 'rb') as fp:
        raw = fp.read().decode('utf8')

    content = string.Template(raw).substitute(**kwargs)

    render_path = path[:-len('.tmpl')] if path.endswith('.tmpl') else path
    with open(render_path, 'wb') as fp:
        fp.write(content.encode('utf8'))
    if path.endswith('.tmpl'):
        os.remove(path)


CAMELCASE_INVALID_CHARS = re.compile('[^a-zA-Z\d]')


def string_camelcase(string):
    return CAMELCASE_INVALID_CHARS.sub('', string.title())
