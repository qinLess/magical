# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: __init__.py.py
    Time: 2021/7/1 上午11:39
-------------------------------------------------
    Change Activity: 2021/7/1 上午11:39
-------------------------------------------------
    Desc: 
"""

import os
from magical.cmdline import generate_spider_project, generate_spider_file


def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    spider_name = 'test_excel'

    generate_spider_project('sync_spider', project_path, spider_name)
    # generate_spider_file('sync_spider', project_path, spider_name)


if __name__ == '__main__':
    main()
