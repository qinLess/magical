# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: handler.py
    Time: 2021/5/7 下午11:23
-------------------------------------------------
    Change Activity: 2021/5/7 下午11:23
-------------------------------------------------
    Desc: 
"""
import threading
from functools import partial

import pika


class MQBase(object):
    """消息队列基类, 该类线程不安全的"""

    def __init__(self, spider, ack=True):
        """当开启手动消息确认, 要考虑消息重入的情况, 默认开启手动消息确认

        Args:
            spider = 爬虫对象
            ack = 是否自动确认消息
        """
        # 使用 线程局部变量，保证rabbit连接线程安全
        self.local = threading.local()

        self.spider = spider
        self.logger = spider.logger

        self._conn = None
        self._properties = pika.BasicProperties(delivery_mode=2, )

        self.virtual_host = spider.settings['MESSAGE_MQ_VIRTUAL_HOST']
        self.prefetch_count = spider.settings['MESSAGE_MQ_PREFETCH_COUNT']
        self.rabbit_config = spider.settings['MESSAGE_MQ_CONFIG']

        self.port = self.rabbit_config['port']
        self.host = self.rabbit_config['host']
        self.username = self.rabbit_config['username']
        self.password = self.rabbit_config['password']

        self.ack = ack

    def close(self):
        try:
            if hasattr(self.local, 'channel'):
                self.local.channel.close()
                self.logger.info('rabbit mq channel closed!')

            if not (self._conn and self._conn.is_open):
                self._conn.close()
                self.logger.info('rabbit mq connection closed!')

        except Exception as e:
            self.logger.error(f'rabbit mq closed error: {e}')

    def _check_channel(self):
        if not hasattr(self.local, 'channel'):
            channel = self._rabbit_mq_init()
            self.local.channel = channel

    def _rabbit_mq_init(self):
        """初始化 连接 rabbit mq"""
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            heartbeat=0
        )
        self._conn = pika.BlockingConnection(parameters)
        channel = self._conn.channel()

        if self.ack:
            channel.confirm_delivery()

        self.logger.info('rabbit mq connection successfully !')

        return channel


class MQSender(MQBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def try_send(self, queue_name, msg):
        try:
            self._check_channel()

            self.local.channel.queue_declare(queue=queue_name, durable=True)
            self.local.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=msg.encode(),
                properties=self._properties
            )
            self.logger.info(f'rabbit MQ 消息推送成功, msg: {msg}')
            success = True
        except Exception as e:
            self.logger.exception(e)
            self.logger.error(f'rabbit MQ 消息推送失败, msg: {msg}')
            success = False

        return success

    def push(self, queue_name, msg):
        ret = self.try_send(queue_name, msg) or self.try_send(queue_name, msg)
        return ret


class MQReceiver(MQBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def basic_ack(self, channel, method):
        return self._conn.add_callback_threadsafe(partial(channel.basic_ack, method.delivery_tag))

    def start(self, queue_name, callback):
        """开始消费"""
        self._check_channel()

        self.local.channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
        self.local.channel.basic_qos(prefetch_count=self.prefetch_count)
        self.local.channel.basic_consume(queue_name, callback, auto_ack=not self.ack)
        self.local.channel.start_consuming()


class RabbitMQHandler(object):
    def __init__(self, spider):
        self.spider = spider

        self.sender = MQSender(spider)
        self.receiver = MQReceiver(spider)

    def close_mq(self):
        # self.sender.close()
        self.receiver.close()

    def producer(self, queue_name, value):
        self.sender.push(queue_name, value)

    def consumer(self, queue_name, callback=None):
        self.receiver.start(queue_name, callback)
