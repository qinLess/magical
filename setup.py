# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: setup.py
    Time: 2021/4/21 下午9:49
-------------------------------------------------
    Change Activity: 2021/4/21 下午9:49
-------------------------------------------------
    Desc: 
"""


from setuptools import setup, find_packages


setup(
    name='magical',
    version='1.1.0',
    description='参照 scrapy 轻量级爬虫框架',
    author='magical developers',
    maintainer='qinjiahu',
    maintainer_email='qinless@qinless.com',
    license='BSD',

    packages=find_packages(exclude=(
        'examples', 'examples.*', 'public', 'public.*', 'test', 'test.*', '.gitee', '.gitee.*',
        'public', 'public.*', 'spiders', 'spiders.*', 'logs', 'logs.*'
    )),

    package_data={
        '': ['*.py.tmpl', '*.json']
    },

    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Framework :: Crawler',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6.*',
    install_requires=[]
)
