# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: settings.py
    Time: 2021/13/13 11:30:06
-------------------------------------------------
    Change Activity: 2021/13/13 11:30:06
-------------------------------------------------
    Desc:
"""
from magical.utils import log_path

# project settings


# -------------------------------------------------------------------------------------------------------------------

# 项目名称
PROJECT_NAME = 'test_douban'

# logger 路径
LOGGER_PATH = log_path(__file__)

# 重试次数
RETRY_COUNT = 10

# 管道中间件，可配置多个
# PIPELINE_MIDDLEWARE_PATH = {
#     "spiders.test_douban.pipeline.DoubanSpiderPipeline": 10
# }

# 下载中间件，可配置多个
DOWNLOAD_MIDDLEWARE_PATH = {
    # "spiders.test_douban.middleware.DuplicateMiddleware": 7,
    # "spiders.test_douban.middleware.HeadersMiddleware": 8,
    # "spiders.test_douban.middleware.ProxyMiddleware": 9,
    "spiders.test_douban.middleware.RequestErrorMiddleware": 10,
    "spiders.test_douban.middleware.DoubanSpiderMiddleware": 100
}

# 爬虫公共类，基类
BASE_SPIDER_PATH = "spiders.test_douban.base_spider.DoubanSpiderBaseSpider"

# user-agent
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

# -------------------------------------------------------------------------------------------------------------------


# default settings

# 下载中间件
DOWNLOADER_PATH = "magical.sync_spider.middleware.download.downloader.Downloader"

# 下载处理中间件
DOWNLOAD_HANDLER_PATH = "magical.sync_spider.middleware.download.handler.DownloadHandler"

# 下载调度器
DOWNLOAD_MIDDLEWARE_MANAGER_PATH = "magical.sync_spider.middleware.download.manager.DownloadMiddlewareManager"

# 下载中间件，可配置多个
# DOWNLOAD_MIDDLEWARE_PATH = {}

# -------------------------------------------------------------------------------------------------------------------

# 管道处理中间件
# PIPELINE_HANDLER_PATH = "magical.sync_spider.middleware.pipeline.handler.PipelineHandler"

# 管道调度器
# PIPELINE_MIDDLEWARE_MANAGER_PATH = "magical.sync_spider.middleware.pipeline.manager.PipelineMiddlewareManager"

# 管道中间件，可配置多个
# PIPELINE_MIDDLEWARE_PATH = {}

# -------------------------------------------------------------------------------------------------------------------
# 暂时不使用，存在问题
# # 去重中间件
# FILTER_DUPLICATE_HANDLER = "magical.sync_spider.middleware.duplicate.handler.DuplicateHandler"
#
# # 去重过滤器
# FILTER_METHOD_MANAGER = "magical.sync_spider.middleware.duplicate.bloom_filter.ScalableBloomFilter"
# # FILTER_METHOD_MANAGER = "magical.sync_spider.middleware.duplicate.expire_filter.ExpireFilter"
#
# # 去重队列，redis， memory = 内存
# FILTER_QUEUE_TYPE = 'redis'
#
# # 去重是否 md5 加密
# FILTER_USE_MD5 = False
#
# # 使用那个 redis 实例 去重，配置连接 name，默认为 red
# FILTER_REDIS_NAME = 'red'
#
# # 去重初始容量
# FILTER_INITIAL_CAPACITY = 100000000
#
# # 去重错误率
# FILTER_ERROR_RATE = 0.00001

# -------------------------------------------------------------------------------------------------------------------

# # rabbit mq 配置
# MESSAGE_MQ_CONFIG = {
#     'username': 'admin',
#     'password': 'admin123',
#     'host': '127.0.0.1',
#     'port': 9999
# }
#
# # rabbit mq 消费批次，每次消费 10 条
# MESSAGE_MQ_PREFETCH_COUNT = 10
#
# # rabbit mq virtual host
# MESSAGE_MQ_VIRTUAL_HOST = 'spider'
#
# # rabbit mq 操作类
# MESSAGE_MQ_HANDLER = 'magical.sync_spider.extends_module.mqs.rabbit_mq.handler.RabbitMQHandler'

# -------------------------------------------------------------------------------------------------------------------

# 爬虫公共类，基类
# BASE_SPIDER_PATH = "magical.sync_spider.common.base_spider.BaseSpider"

# 爬虫工具类
SPIDER_UTIL_PATH = "magical.sync_spider.common.spider_util.SpiderUtil"

# 代理IP中间件
# redis IP 获取
# PROXY_HANDLER = 'magical.sync_spider.common.proxy_handler.GetRedisProxy'
# # 芝麻代理 IP
# PROXY_HANDLER = 'magical.sync_spider.common.proxy_handler.GetZhiMaProxy'

# 邮件
EMAIL_HANDLER = 'magical.sync_spider.common.email_handler.EmailHandler'

# post ger sql 操作类
POST_GRE_SQL_HANDLER = 'magical.sync_spider.databases.post_gre_sql_pool.PostGreHandle'

# mysql 操作类
MYSQL_HANDLER = 'magical.sync_spider.databases.mysql_pool.MysqlHandler'

# redis 操作类
REDIS_HANDLER = 'magical.sync_spider.databases.red_pool.RedisHandler'

# -------------------------------------------------------------------------------------------------------------------

# 初始化 代理 IP 数量
PROXY_NUM = 5

# 重试次数
# RETRY_COUNT = 3

# 包含一下状态吗，重试
RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

# 忽略 ssl 验证
REQUEST_VERIFY = False

# 请求超时时间
REQUEST_TIMEOUT = 30

# 消费者线程数
CONSUMER_THREAD_NUM = 10

# -------------------------------------------------------------------------------------------------------------------

"""
数据库配置

单个数据库
REDIS_CONFIG = {
    'host': '',
    'host': '',
    'db': '',
    'user': '',
    'password': '',
    'decode_responses': True
}
使用:
    red 默认变量名称
    self.red.get('key1')
    spider.red.get('key1')

多个数据库
REDIS_CONFIG = [
    {
        'name': 'name1',
        'host': '',
        'host': '',
        'db': '',
        'user': '',
        'password': '',
        'decode_responses': True
    },
    {
        'name': 'name2',
        'host': '',
        'host': '',
        'db': '',
        'user': '',
        'password': '',
        'decode_responses': True
    },
]
使用:
    self.name1.get('key1')
    spider.name1.get('key1')

    self.name2.get('key1')
    spider.name2.get('key1')
"""
