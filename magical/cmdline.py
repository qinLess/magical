# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: cmdline.py
    Time: 2021/4/14 下午3:09
-------------------------------------------------
    Change Activity: 2021/4/14 下午3:09
-------------------------------------------------
    Desc: 
"""
import os
import string
import sys
import datetime
from shutil import copy2, copystat
from os.path import join, exists, abspath, dirname

from magical.template import render_template_file, string_camelcase

TEMPLATES_TO_RENDER = [
    ('${spider_name}', 'spiders', '__init__.py.tmpl'),
    ('${spider_name}', 'base_spider.py.tmpl'),
    ('${spider_name}', 'middleware.py.tmpl'),
    ('${spider_name}', 'settings.py.tmpl')
]


def _copytree(src, dst):
    """复制文件

    Args:
        src: 模版文件路径(str)
        dst: 项目路径(str)
    Returns:
    """
    if not exists(dst):
        os.makedirs(dst)

    names = os.listdir(src)

    for name in names:
        if name == 'spider.py.tmpl':
            continue

        if name == '__init__.py':
            continue

        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)

        if os.path.isdir(src_name):
            _copytree(src_name, dst_name)

        else:
            copy2(src_name, dst_name)

    copystat(src, dst)


def generate_spider_project(spider_type, project_path=None, spider_name=None):
    """生成项目爬虫文件

    Args:
        spider_type: 爬虫类型（sync_spider, async_spider）
        project_path: 项目路径
        spider_name: 爬虫名称
    """
    if not spider_type:
        sys.exit('spider_type is not null')

    if not project_path:
        sys.exit('project_path is not null')

    if not spider_name:
        sys.exit('spider_name is not null')

    templates_dir = abspath(join(dirname(__file__), f'templates/{spider_type}'))
    _copytree(templates_dir, join(abspath(project_path)))
    copy2(join(templates_dir, 'spider.py.tmpl'), join(abspath(project_path), 'spiders', f'{spider_name}.py.tmpl'))

    s_path = abspath(project_path).split('/')
    spider_path = '.'.join(s_path[s_path.index('spiders'):])
    settings_path = spider_path + '.settings'
    project_name = s_path[s_path.index('spiders') + 1]

    TEMPLATES_TO_RENDER.append(('${spider_name}', 'spiders', f'{spider_name}.py.tmpl'))

    for paths in TEMPLATES_TO_RENDER:
        path = join(*paths)

        tpl_file = string.Template(path).substitute(spider_name=project_path)

        render_template_file(
            tpl_file,
            project_name=project_name,
            settings_path=settings_path,
            spider_path=spider_path,
            spider_name=spider_name,
            create_time=datetime.datetime.now().strftime('%Y/%d/%d %H:%M:%S'),
            SpiderName=string_camelcase(spider_name),
        )


def generate_spider_file(spider_type, project_path=None, spider_name=None):
    """生成爬虫文件

    Args:
        spider_type: 爬虫类型（sync_spider, async_spider）
        project_path: 项目路径
        spider_name: 爬虫名称
    """
    if not spider_type:
        sys.exit('spider_type is not null')

    if not project_path:
        sys.exit('project_path is not null')

    if not spider_name:
        sys.exit('spider_name is not null')

    templates_dir = abspath(join(dirname(__file__), f'templates/{spider_type}'))
    copy2(join(templates_dir, 'spider.py.tmpl'), join(abspath(project_path), 'spiders', f'{spider_name}.py.tmpl'))

    s_path = abspath(project_path).split('/')
    spider_path = '.'.join(s_path[s_path.index('spiders'):])
    settings_path = spider_path + '.settings'

    path = join(*('${spider_name}', 'spiders', f'{spider_name}.py.tmpl'))

    tpl_file = string.Template(path).substitute(spider_name=project_path)

    render_template_file(
        tpl_file,
        settings_path=settings_path,
        spider_path=spider_path,
        spider_name=spider_name,
        create_time=datetime.datetime.now().strftime('%Y/%d/%d %H:%M:%S'),
        SpiderName=string_camelcase(spider_name),
    )


if __name__ == '__main__':
    generate_spider_project('async_spider', '/Users/qinjiahu/Desktop/project/gn/spider_project/test/test1', 'test1')
