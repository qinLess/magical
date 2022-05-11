# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: spider.py
    Time: 2021/4/10 下午4:55
-------------------------------------------------
    Change Activity: 2021/4/10 下午4:55
-------------------------------------------------
    Desc: 
"""
import copy
import json
import time
import importlib
from queue import Queue

import threading
import requests
from sqlalchemy import create_engine

from magical.utils import load_objects
from magical.sync_spider.common.log_setting import get_logger

from magical.sync_spider.databases.init_db import InitDatabase

from magical.sync_spider.config.settings import Settings
from magical.sync_spider.http.response import Response
from magical.sync_spider.http.request import Request


# 爬虫初始化
class InitSpider(object):
    name = 'base_init_spider'

    spider_start_time = time.time()

    this = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.custom_setting = kwargs.get('custom_setting', {})
        self.settings_path = kwargs.get('settings_path')
        self.common_settings_path = kwargs.get('common_settings_path')

        self.__load_settings(self.custom_setting)

        self.logger = get_logger(self)
        self.__load_dbs()

        self.email_handler = load_objects(self.settings['EMAIL_HANDLER'])
        self.spider_util = load_objects(self.settings['SPIDER_UTIL_PATH'])(self)

        if self.settings['PROXY_HANDLER']:
            self.proxy = load_objects(self.settings['PROXY_HANDLER'])(self)

        if self.settings['FILTER_DUPLICATE_HANDLER']:
            self.duplicate = load_objects(self.settings['FILTER_DUPLICATE_HANDLER'])(self)

        InitSpider.this = self

    def __load_settings(self, custom_setting={}):
        self.settings = Settings()
        self.settings.set_dict(custom_setting)
        if self.settings_path:
            try:
                self.settings.load_config(importlib.import_module(self.common_settings_path))
            except Exception as e:
                pass
            self.settings.load_config(importlib.import_module(self.settings_path))

    def __load_dbs(self):
        self.dbs = InitDatabase(self).dbs

        for db in self.dbs:
            setattr(self, db['name'], db['instance'])

    def __close_dbs(self):
        for db in self.dbs:
            db['instance'] and db['instance'].close_pool()

    def test_ip(self, proxy):
        res = None
        try:
            res = requests.get('http://www.httpbin.org/ip', proxies=proxy)
            res_json = res.json()

            if res_json.get('origin') in proxy.get('http', proxy.get('https', )):
                self.logger.info(f'可用代理: {proxy}')
                return True

            else:
                self.logger.error(f'不可用代理: {proxy}')

        except Exception as e:
            self.logger.error(f'测试代理异常: {proxy}, error: {e}, res: {res and res.text}', exc_info=True)

    def close_spider(self):
        self.__close_dbs()
        self.logger.info(f'Time usage: {time.time() - self.spider_start_time}')
        self.logger.info(f'Spider finished!')
        self.logger.info(f'Close Spider!')

    @staticmethod
    def this_close_spider():
        InitSpider.this.close_spider()

    @staticmethod
    def get_create_engine(db_type, name, settings_path):
        """获取数据库 create_engine 连接，用于 pandas

        Args:
            db_type: mysql or post_gre
            name: 数据库名称
            settings_path: 配置文件路径
        """
        custom_settings = importlib.import_module(settings_path)

        configs = getattr(custom_settings, f'{db_type.upper()}_CONFIG')

        if isinstance(configs, list):
            dbs = list(filter(lambda x: x['name'] == name, configs))
            if len(dbs) == 0:
                raise KeyError(f'{db_type} {name} 数据库 不存在')

            else:
                config = dbs[0]
        else:
            config = configs

        db = config['db']
        user = config['user']
        host = config['host']
        port = config['port']
        password = config['password']

        if db_type == 'post_gre':
            db_engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

        else:
            db_engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4')

        return db_engine


# 爬虫基类
class BaseSyncSpider(object):
    name = 'base_sync_spider'
    spider_data = {}
    default_custom_setting = {}
    settings_path = None
    base_spider = None
    common_settings_path = 'spiders.common.settings'

    def __init__(self, *args, **kwargs):
        self.custom_setting = kwargs.get('custom_setting', {})
        self.custom_setting.update(self.default_custom_setting)

        kwargs['custom_setting'] = self.custom_setting
        kwargs['name'] = self.name
        kwargs['settings_path'] = self.settings_path
        kwargs['common_settings_path'] = self.common_settings_path

        if not kwargs.get('init_spider'):
            self.init_spider = InitSpider(*args, **kwargs)

        else:
            self.init_spider = kwargs.get('init_spider')

        self.settings = Settings()
        self.settings.set_dict({k: v.value for k, v in self.init_spider.settings.attrs.items()})
        self.settings.set_dict(copy.deepcopy(self.custom_setting))

        self.download_cls = load_objects(self.settings['DOWNLOADER_PATH'])(self)
        self.pipeline_cls = load_objects(self.settings['PIPELINE_HANDLER_PATH'])(self)
        self.base_spider = load_objects(self.settings['BASE_SPIDER_PATH'])(self)

        self.__load_mq()

        if self.settings.get('SPIDER_INIT_HANDLER'):
            self.spider_init = load_objects(self.settings['SPIDER_INIT_HANDLER'])(self)

    def close_message_mq(self):
        message_mq = getattr(self, 'message_mq')
        if message_mq:
            message_mq.close_mq()

    def __load_mq(self):
        message_mq_handler = self.settings['MESSAGE_MQ_HANDLER']
        if message_mq_handler:
            setattr(self, 'message_mq', load_objects(message_mq_handler)(self))

    def __getattr__(self, item: str):

        if hasattr(self.init_spider, item):
            return getattr(self.init_spider, item)

        elif self.base_spider and hasattr(self.base_spider, item):
            return getattr(self.base_spider, item)

        else:
            self.logger.error(f'{item} 属性不在，base_spider or init_spider')
            return None

    def __download(self, request: Request) -> Response:
        response = self.download_cls.fetch(request)
        return response

    def download(self, request: Request = None, **kwargs) -> Response:
        if not isinstance(request, Request):
            request = Request(**kwargs)
        try:
            response = self.__download(request)
        except AttributeError as exc:
            self.logger.error(f'AttributeError: {str(exc)}', exc_info=True)
            self.logger.warning('find a error,post to error back.')
        except Exception as exc:
            self.logger.error(f'AttributeError: {str(exc)}', exc_info=True)
        else:
            if isinstance(response, Request):
                return self.download(response)

            return response

    def pipeline(self, item, **kwargs):
        return self.pipeline_cls.pipeline(item, **kwargs)

    def test_ip(self, proxy: dict) -> bool:
        return self.init_spider.test_ip(proxy)

    @staticmethod
    def create_thread(func, **kwargs):
        t = threading.Thread(target=func, args=(kwargs,))
        t.start()
        return t

    @staticmethod
    def create_engine(db_type, name, settings_path):
        return InitSpider.get_create_engine(db_type, name, settings_path)


# redis 订阅者爬虫类
class RedisMessageMQSpider(BaseSyncSpider):
    name = 'redis_message_mq_spider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.consumer_thread_num = self.settings['CONSUMER_THREAD_NUM'] or 10
        self.spider_queue = Queue(100)

    def start_spider(self):
        raise NotImplementedError

    def start(self):
        self.logger.info('Start Spider!')

        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'redis_message_mq_spider.start.error: {e}', exc_info=True)

        finally:
            self.close_spider()

    def start_thread(self):
        """启动爬虫，适用于多线程"""
        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'redis_message_mq_spider.start_thread.error: {e}', exc_info=True)

    def __consumer_queue(self, func):
        while True:
            msg = self.spider_queue.get()
            try:
                self.logger.info(f'spider_queue.msg: {msg}')
                func(msg)

            except Exception as e:
                self.logger.exception(e)

            self.spider_queue.task_done()

    def __consumer_mq(self, key):
        redis_sub = self.red_mq.subscribe(key)
        msgs = redis_sub.listen()

        for msg in msgs:
            if msg['type'] == 'message':
                self.spider_queue.put(json.loads(msg['data']))

    def producer_mq(self, key, value=None, values=None):
        if isinstance(values, list):
            for i in values:
                if isinstance(i, dict):
                    i = json.dumps(i, ensure_ascii=False)

                self.red_mq.public(key, i)

        else:
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)

            self.red_mq.public(key, value)

    def producer(self, func=None, **kwargs):
        t = threading.Thread(target=func, args=(kwargs,))
        t.start()
        return t

    def consumer_mq(self, key):
        t = threading.Thread(target=self.__consumer_mq, args=(key,))
        t.start()
        return t

    def consumer_queue(self, func, thread_num=None):
        for index in range(thread_num or self.consumer_thread_num):
            consumer_thread = threading.Thread(target=self.__consumer_queue, args=(func,))
            consumer_thread.daemon = True
            consumer_thread.start()


# rabbit MQ 爬虫类
class RabbitMessageMQSpider(BaseSyncSpider):
    name = 'rabbit_message_mq_spider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.consumer_thread_num = self.settings['CONSUMER_THREAD_NUM'] or 10
        self.spider_queue = Queue(100)

        self.fail_spider_queue = Queue(100)

    def start_spider(self):
        raise NotImplementedError

    def start(self):
        self.logger.info('Start Spider!')

        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'rabbit_message_mq_spider.start.error: {e}', exc_info=True)

        finally:
            self.close_message_mq()
            self.close_spider()

    def start_thread(self):
        """启动爬虫，适用于多线程"""
        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'rabbit_message_mq_spider.start_thread.error: {e}', exc_info=True)

    def __consumer_queue(self, func):
        while True:
            channel, method, properties, body = self.spider_queue.get()
            try:
                msg = json.loads(body)

            except json.decoder.JSONDecodeError:
                msg = body.decode()

            try:
                self.logger.info(f'spider_queue.msg: {msg}')

                if func(msg):
                    self.logger.info(f'rabbit mq 消费成功: {msg}')

                else:
                    self.logger.error(f'rabbit mq 消费失败: {msg}')
                    self.fail_spider_queue.put(msg)

            except Exception as e:
                self.logger.exception(e)
                self.fail_spider_queue.put(msg)

            finally:
                self.message_mq.receiver.basic_ack(channel, method)
                self.spider_queue.task_done()

    def consumer_queue(self, func, thread_num=None):
        for index in range(thread_num or self.consumer_thread_num):
            consumer_thread = threading.Thread(target=self.__consumer_queue, args=(func,))
            consumer_thread.daemon = True
            consumer_thread.start()

    def __consumer_mq_callback(self, channel, method, properties, body):
        self.spider_queue.put((channel, method, properties, body))

    def consumer_mq(self, key):
        t = threading.Thread(target=self.message_mq.consumer, args=(key, self.__consumer_mq_callback))
        t.start()
        return t

    def producer_mq(self, key=None, value=None, values=None):
        if isinstance(values, list):
            for i in values:
                if isinstance(i, dict):
                    i = json.dumps(i, ensure_ascii=False)

                self.message_mq.producer(key, i)

        else:
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)

            self.message_mq.producer(key, value)

    def get_queue_len(self):
        return self.spider_queue.qsize()


# 单线程爬虫类
class SyncSpider(BaseSyncSpider):
    name = 'sync_spider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.consumer_thread_num = self.settings['CONSUMER_THREAD_NUM'] or 10
        self.spider_queue = Queue(1000)

    def start_spider(self):
        raise NotImplementedError

    def start(self):
        """启动爬虫，适用于单线程"""
        self.logger.info('Start Spider!')

        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'sync_spider.start.error: {e}', exc_info=True)

        finally:
            self.close_spider()

    def start_thread(self):
        """启动爬虫，适用于多线程"""
        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'sync_spider.start_thread.error: {e}', exc_info=True)

    def start_mq(self):
        """启动爬虫，适用于消息队列, redis mq"""
        try:
            self.start_spider()

        except Exception as e:
            self.logger.error(f'sync_spider.start_mq.error: {e}', exc_info=True)

    def __producer(self, items):
        for item in items:
            self.spider_queue.put(item)

        self.spider_queue.join()

    def producer(self, items=[], func=None, **kwargs):

        if func:
            t = threading.Thread(target=func, args=(kwargs,))
        else:
            t = threading.Thread(target=self.__producer, args=(items,))

        t.start()
        return t

    def __consumer(self, func, queue):
        spider_queue = queue if queue else self.spider_queue

        while True:
            msg = spider_queue.get()
            try:
                # self.logger.info(f'spider_queue.msg: {msg}')
                func(msg)

            except Exception as e:
                self.logger.exception(e)

            spider_queue.task_done()

    def consumer(self, func, thread_num=None, queue=None):
        for index in range(thread_num or self.consumer_thread_num):
            consumer_thread = threading.Thread(target=self.__consumer, args=(func, queue))
            consumer_thread.daemon = True
            consumer_thread.start()


# 多线程爬虫类
class ThreadSyncSpider(object):
    def __init__(self, items, spider_cls, *args, **kwargs):
        kwargs['name'] = spider_cls.name
        kwargs['settings_path'] = spider_cls.settings_path
        kwargs['custom_setting'] = spider_cls.default_custom_setting

        self.init_spider = InitSpider(*args, **kwargs)

        self.items = items
        self.spider_cls = spider_cls

        self.tasks = []

    def __start(self, item):
        self.spider_cls(init_spider=self.init_spider, **item).start_thread()

    def start(self):
        InitSpider.this.logger.info('Start Spider!')

        try:
            for item in self.items:
                t = threading.Thread(target=self.__start, args=(item,))
                t.start()
                self.tasks.append(t)

            for task in self.tasks:
                task.join()

        except Exception as e:
            InitSpider.this.logger.error(f'sync_spider.start.error: {e}', exc_info=True)

        finally:
            InitSpider.this_close_spider()
