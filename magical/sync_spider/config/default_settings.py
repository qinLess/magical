# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: default_settings.py
    Time: 2021/4/10 下午5:19
-------------------------------------------------
    Change Activity: 2021/4/10 下午5:19
-------------------------------------------------
    Desc: 
"""

# -------------------------------------------------------------------------------------------------------------------

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
#     'port': 18097
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

# 下载中间件
DOWNLOADER_PATH = "magical.sync_spider.middleware.download.downloader.Downloader"

# 下载处理中间件
DOWNLOAD_HANDLER_PATH = "magical.sync_spider.middleware.download.handler.DownloadHandler"

# 下载调度器
DOWNLOAD_MIDDLEWARE_MANAGER_PATH = "magical.sync_spider.middleware.download.manager.DownloadMiddlewareManager"

# 中间件，可配置多个，默认是重试中间件
DOWNLOAD_MIDDLEWARE_PATH = {}

# -------------------------------------------------------------------------------------------------------------------

# 管道处理中间件
PIPELINE_HANDLER_PATH = "magical.sync_spider.middleware.pipeline.handler.PipelineHandler"

# 管道调度器
PIPELINE_MIDDLEWARE_MANAGER_PATH = "magical.sync_spider.middleware.pipeline.manager.PipelineMiddlewareManager"

# 管道中间件，可配置多个
PIPELINE_MIDDLEWARE_PATH = {}

# -------------------------------------------------------------------------------------------------------------------

# 爬虫公共类，基类
BASE_SPIDER_PATH = "magical.sync_spider.common.base_spider.BaseSpider"

# 爬虫工具类
SPIDER_UTIL_PATH = "magical.sync_spider.common.spider_util.SpiderUtil"

# 邮件
EMAIL_HANDLER = 'magical.sync_spider.common.email_handler.EmailHandler'

# post ger sql 操作类
POST_GRE_SQL_HANDLER = 'magical.sync_spider.databases.post_gre_sql_pool.PostGreHandle'

# mysql 操作类
MYSQL_HANDLER = 'magical.sync_spider.databases.mysql_pool.MysqlHandler'

# redis 操作类
REDIS_HANDLER = 'magical.sync_spider.databases.red_pool.RedisHandler'

# 代理IP中间件
# redis IP 获取
# PROXY_HANDLER = 'magical.sync_spider.common.proxy_handler.GetRedisProxy'
# # 芝麻代理 IP
# PROXY_HANDLER = 'magical.sync_spider.common.proxy_handler.GetZhiMaProxy'

# -------------------------------------------------------------------------------------------------------------------

# 初始化 代理 IP 数量
PROXY_NUM = 5

# 重试次数
RETRY_COUNT = 3

# 包含一下状态吗，重试
RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

# 忽略 ssl 验证
REQUEST_VERIFY = False

# 请求超时时间
REQUEST_TIMEOUT = 30

# 5s盾，delay 时间
SCRAPER_DELAY = 30

# 消费者线程数
CONSUMER_THREAD_NUM = 10



