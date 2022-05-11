# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: test_excel.py
    Time: 2021/01/01 11:40:25
-------------------------------------------------
    Change Activity: 2021/01/01 11:40:25
-------------------------------------------------
    Desc:
"""
import os
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(file_path)

from magical.sync_spider import SyncSpider, load_files, run_spider


class TestExcelSpider(SyncSpider):
    name = 'test_excel'
    settings_path = 'spiders.test_spider.settings'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        custom_setting = {}
        kwargs.update(dict(custom_setting=custom_setting))
        super().__init__(*args, **kwargs)

        self.excel = load_files(self.settings['EXCEL'])

    def start_spider(self):
        data_list = [
            {'desc': 'desc1', 'name': 'name1', 'plat': 'plat1'},
            {'desc': 'desc2', 'name': 'name2', 'plat': 'plat2'},
            {'desc': 'desc3', 'name': 'name3', 'plat': 'plat3'},
            {'desc': 'desc4', 'name': 'name4', 'plat': 'plat4'},
            {'desc': 'desc5', 'name': 'name5', 'plat': 'plat5'},
        ]

        title = {'desc': '描述', 'name': '店铺名称', 'plat': '渠道'}
        excel_name = 'test'
        excel_file_path = '../static/test.xls'
        self.excel.write_excel(data_list, title, excel_name, excel_file_path)


if __name__ == '__main__':
    run_spider(TestExcelSpider)
