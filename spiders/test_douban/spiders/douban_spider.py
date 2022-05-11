# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: douban_spider.py
    Time: 2021/13/13 11:30:06
-------------------------------------------------
    Change Activity: 2021/13/13 11:30:06
-------------------------------------------------
    Desc:
"""
import json
import os
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(file_path)

from magical.sync_spider import SyncSpider, run_spider, load_files


class DoubanSpiderSpider(SyncSpider):
    name = 'douban_spider'
    settings_path = 'spiders.test_douban.settings'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        custom_setting = {}
        kwargs.update(dict(custom_setting=custom_setting))
        super().__init__(*args, **kwargs)

        self.ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

        self.excel = load_files(self.settings['EXCEL'])

    def get_list(self, start=0, limit=100, tag='热门'):

        self.logger.info(f'start: {start}, tag: {tag}')

        headers = {
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/tv/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.ua,
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            'type': 'tv',
            'tag': tag,
            'sort': 'recommend',
            'page_limit': limit,
            'page_start': start
        }
        url = 'https://movie.douban.com/j/search_subjects'
        response = self.download(url=url, headers=headers, params=params)
        subjects = response.json().get('subjects', [])

        if len(subjects) > 0:
            self.red.sadd('dbList', *[json.dumps(i, ensure_ascii=False) for i in subjects])

        if len(subjects) < 100:
            return

        else:
            start += 100
            return self.get_list(start=start)

    def get_info(self, list_info):
        info_url = list_info['url']
        headers = {
            'Host': 'movie.douban.com',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'User-Agent': self.ua,
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            response = self.download(url=info_url, headers=headers)

            # 年份
            year = response.re.findall('<span class="year">\((.*?)\)</span>')
            print('year: ', year)

            # 导演
            dao_yan = response.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
            print('dao_yan: ', dao_yan)

            # 编剧
            bian_ju = response.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
            print('bian_ju: ', bian_ju)

            # 主演
            zhu_yan = response.re.findall('<a href=".*?" rel="v:starring">(.*?)</a>')
            print('zhu_yan: ', zhu_yan)

            # 类型
            lei_xing = response.re.findall('<span property="v:genre">(.*?)</span>')
            print('lei_xing: ', lei_xing)

            # 制片国家/地区
            di_qu = response.re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>')
            print('di_qu: ', di_qu)

            # 语言
            yu_yan = response.re.findall('<span class="pl">语言:</span> (.*?)<br/>')
            print('yu_yan: ', yu_yan)

            # 首播
            shou_bo = response.xpath('//*[@id="info"]/span[10]/text()')
            print('shou_bo: ', shou_bo)

            # 集数
            ji_shu = response.re.findall('<span class="pl">集数:</span> (.*?)<br/>')
            print('ji_shu: ', ji_shu)

            # 单集片长
            dan_ji = response.re.findall('<span class="pl">单集片长:</span> (.*?)<br/>')
            print('dan_ji: ', dan_ji)

            # 豆瓣总评分
            score = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
            print('score: ', score)

            # 评价人数
            comment_num = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
            print('comment_num: ', comment_num)

            # 短评数
            duan_ping_num = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')
            print('duan_ping_num: ', duan_ping_num)

            # 小组讨论数

            # 剧情简介
            desc = response.xpath('//*[@id="link-report"]/span/text()')
            print('desc: ', desc)

            # 标签
            tag = response.xpath('//*[@id="content"]/div[2]/div[2]/div[4]/div/a/text()')
            print('tag: ', tag)

            # 播放平台

            # 在看人数
            zai_kan = response.xpath('//*[@id="subject-others-interests"]/div/a[1]/text()')
            print('zai_kan: ', zai_kan)

            # 看过人数
            kan_guo = response.xpath('//*[@id="subject-others-interests"]/div/a[2]/text()')
            print('kan_guo: ', kan_guo)

            # 想看人数
            xiang_kan = response.xpath('//*[@id="subject-others-interests"]/div/a[3]/text()')
            print('xiang_kan: ', xiang_kan)

            data = {
                'url': list_info['url'],
                'year': ', '.join(year),
                'dao_yan': ', '.join(dao_yan),
                'bian_ju': ', '.join(bian_ju),
                'zhu_yan': ', '.join(zhu_yan),
                'lei_xing': ', '.join(lei_xing),
                'di_qu': ', '.join(di_qu),
                'yu_yan': ', '.join(yu_yan),
                'shou_bo': ', '.join(shou_bo),
                'ji_shu': ', '.join(ji_shu),
                'dan_ji': ', '.join(dan_ji),
                'score': ', '.join(score),
                'comment_num': ', '.join(comment_num),
                'duan_ping_num': ', '.join(duan_ping_num),
                'desc': (', '.join(desc)).strip(),
                'tag': ', '.join(tag),
                'zai_kan': ', '.join(zai_kan),
                'kan_guo': ', '.join(kan_guo),
                'xiang_kan': ', '.join(xiang_kan),
            }

            self.red.sadd('dbInfo', json.dumps(data, ensure_ascii=False))

        except Exception as e:
            self.logger.info(f'error: {e}, list_info: {list_info}')

    def to_excel(self, items):
        def handler(x):
            if not x.get('year'):
                return False

            if not x.get('dao_yan'):
                return False

            return True

        data_list = list(filter(handler, map(lambda x: json.loads(x), items)))
        title = {
            'url': '链接',
            'year': '年份',
            'dao_yan': '导演',
            'bian_ju': '编剧',
            'zhu_yan': '主演',
            'lei_xing': '类型',
            'di_qu': '制片国家/地区',
            'yu_yan': '语言',
            'shou_bo': '首播',
            'ji_shu': '集数',
            'dan_ji': '单集片长',
            'score': '豆瓣评分（总分）',
            'comment_num': '评价人数（总分）',
            'duan_ping_num': '短评数',
            'desc': '剧情简介',
            'tag': '标签',
            'zai_kan': '在看人数',
            'kan_guo': '看过人数',
            'xiang_kan': '想看人数',
        }
        excel_name = '豆瓣电影'

        self.excel.write_excel(data_list, title, excel_name, '../static/豆瓣电影.xls')

    def start_spider(self):
        # self.get_list()

        # data_list = list(self.red.smembers('dbList'))
        # for i in data_list:
        #     self.get_info(json.loads(i))

        self.to_excel(list(self.red.smembers('dbInfo')))


if __name__ == '__main__':
    run_spider(DoubanSpiderSpider)
