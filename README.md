## 简介

**magical** 轻量级爬虫框架, 模仿 scrapy 开发，没有 scrapy 复杂，抛弃了 yield 跟 回掉函数，流程简单化，全部可自定义，框架只是简单封装了一些常用函数

### 项目文件:  
- `spiders`     爬虫列表文件夹
- `settings`    爬虫配置文件
- `middleware`  中间件文件
- `pipeline`    管道文件
- `base_spdier`

### spider 提供3个爬虫类：
- `SyncSpider` 单线程爬虫
- `RedisMessageMQSpider` redis 发布者订阅者模式爬虫
- `RabbitMessageMQSpider` rabbitMQ 生产者消费者爬虫
- `ThreadSyncSpider` 多线程爬虫，启动多个线程，去实例化以上三种爬虫类

**sync_spider**  `requests`同步版本  
**async_spider**  `aiohttp`异步版本 (问题较多，已放弃开发)

## 创建项目 (需要先创建 spiders 文件夹，执行以下代码可自动生成代码文件)
```python
import os
from magical.cmdline import generate_spider_project, generate_spider_file


def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    spider_name = 'test_spider_pipelines'
    
    # 创建单个爬虫文件
    generate_spider_file('sync_spider', project_path, spider_name)
    
    # 创建爬虫项目
    # generate_spider_project('sync_spider', project_path, spider_name)


if __name__ == '__main__':
    main()
```


## Spider
```python
from magical.sync_spider import run_spider, SyncSpider, Request


class TestSpider(SyncSpider):
    name = 'test_spider'
    settings_path = 'spiders.test.settings.py'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        custom_setting = {}
        kwargs.update(dict(custom_setting=custom_setting))
        super().__init__(*args, **kwargs)

    def start_spider(self):
        self.logger.info(f'Hello {self.name}')
        
        # 发起request请求
        request = Request(url='http://www.baidu.com/')
        response = self.download(request)

        title = response.re.findall('<title>(.*?)</title>')
        self.logger.info(f'title: {title}')

        data = {'title': title[0]}

        # 调用 pipeline 处理数据，返回 True or False
        pip_res = self.pipeline(data)
        print('pip_res: ', pip_res)
        
        # 调用 redis 
        self.red.get('key1')

        # 调用 mysql
        self.mysql.select('select * from test;')

        # 调用 postgresql 
        self.post_gre.select('select * from test;')


if __name__ == '__main__':
    run_spider(TestSpider)
```

## Database
数据库配置, redis 为例
- 单个数据库
```python
REDIS_CONFIG = {
    'host': '',
    'host': '',
    'db': '',
    'user': '',
    'password': '',
    'decode_responses': True
}

"""red 默认变量名称
Usage:
    self.red.get('key1')
    spider.red.get('key1') 
"""
```
- 多个数据库
```python
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
    }
]
"""
Usage:
    self.name1.get('key1')
    spider.name1.get('key1')

    self.name2.get('key1')
    spider.name2.get('key1')
"""
```
- RedisPool 使用 (默认访问名称 red, 如果有多个连接 通过 name 字段访问)
```python

self.red.get('key1')
self.red.set('key1', 'value1')
```

- MysqlPool 使用 (默认访问名称 mysql, 如果有多个连接 通过 name 字段访问)
```python

# 执行 sql 
self.mysql.execute('select * from test;')

# 查询 sql 
self.mysql.select('select * from test;')

# 插入单条数据
data = {
    'feild1': 'data1',
    'field2': 'data2'
}
self.mysql.insert_dict(table_name='table1', info_dict=data, ignore=False, replace=False)

# 插入多条数据
data = [
    {
        'feild1': 'data1',
        'field2': 'data2'
    },
    {
        'feild1': 'data1',
        'field2': 'data2'
    }
]
self.mysql.insert_list(table_name='table1', info_list=data, ignore=False, replace=False)
```

- PostGreSqlPool 使用 (默认访问名称 post_gre, 如果有多个连接 通过 name 字段访问)
```python

# 执行 sql 
self.post_gre.execute('select * from test;')

# 查询 sql 
self.post_gre.select('select * from test;')

# 插入单条数据 (indexes = 表的唯一索引，用于过滤已存在的数据)
data = {
    'feild1': 'data1',
    'field2': 'data2'
}
self.post_gre.insert_conflict_dict(table_name='table1', info_dict=data, indexes=False)

# 插入多条数据 (indexes = 表的唯一索引，用于过滤已存在的数据)
data = [
    {
        'feild1': 'data1',
        'field2': 'data2'
    },
    {
        'feild1': 'data1',
        'field2': 'data2'
    }
]
self.post_gre.insert_conflict_list(table_name='table1', info_list=data, indexes=False)
```

## Download Middleware  
```python

import requests

from magical.sync_spider.extends_module.base_module.downloader import DownloaderMiddleware


class DuplicateMiddleware(DownloaderMiddleware):
    """去重中间件"""

    def __init__(self, spider):
        super().__init__(spider)

    def process_request(self, request):

        if request.meta.get('is_filter'):
            # 0 == 不存在，1 == 存在
            if self.duplicate.get(**request.meta['filter_info']) != 0:
                return None

        return request

    def process_response(self, request, response):

        if response and request.meta.get('is_filter'):
            # 请求成功添加到，去重种子列表里。 0 == 已存在，1 == 不存在，添加成功
            if self.duplicate.add(**request.meta['filter_info']) == 1:
                pass

        return response


class HeadersMiddleware(DownloaderMiddleware):
    """请求头中间件，User-Agent 随机切换"""

    def __init__(self, spider):
        super().__init__(spider)

    def process_request(self, request):
        request.headers.update({
            'Connection': 'close',
            'user-agent': self.spider.spider_util.random_ua()
        })
        return request


class ProxyMiddleware(DownloaderMiddleware):
    """代理 IP 中间件"""

    def __init__(self, spider):
        super().__init__(spider)
        
        # 初始化代理 IP，num 初始化几条
        # self.proxy_handler(num=1)

    def process_request(self, request):
        # 获取一条代理 IP
        # request.meta['proxy'] = self.proxy.get_proxy()
        return request

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        self.logger.error(f'ProxyMiddleware.process_exception: {exception}, request: {request}', exc_info=True)

        if isinstance(
            exception,
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
            )
        ):
            self.logger.error(f'ProxyMiddleware - 请求异常重试 - request: {request}')
            time.sleep(random.randint(3, 5))
            self.proxy.proxy_handler(request, num=1)
            return self._retry(request)

        elif isinstance(exception, requests.exceptions.HTTPError):
            self.logger.error(f'ProxyMiddleware - requests.exceptions.HTTPError - request: {request}')
            return None

        elif isinstance(exception, requests.exceptions.ChunkedEncodingError):
            self.logger.error(f'ProxyMiddleware - requests.exceptions.ChunkedEncodingError - request: {request}')
            return None

        elif isinstance(exception, requests.exceptions.SSLError):
            self.logger.error(f'ProxyMiddleware - requests.exceptions.SSLError - request: {request}')
            return None

        return exception


class TestSpiderMiddleware(DownloaderMiddleware):
    """爬虫中间件"""

    def __init__(self, spider):
        super().__init__(spider)

    def process_request(self, request):
        return request

    def process_response(self, request, response):
        if not request.use_middleware:
            return response

        return response

    def process_exception(self, request, exception):
        self.logger.exception(f'TestSpiderMiddleware.process_exception: {exception}, request: {request}')
        return exception
```

## Pipeline Middleware  
```python
class TestSpiderPipeline(PipelineMiddleware):

    def __init__(self, spider):
        super().__init__(spider)

    def process_item(self, item, **kwargs):
        """数据处理

        Args:
            item  : 要处理的数据
            kwargs:
                table_name: 表名称
                replace   : True or False (mysql 数据库使用)
                ignore    : True or False (mysql 数据库使用)
                indexes   : 数据库表唯一索引字段 (PostGreSql 数据库使用)

        Return:
            返回的数据类型如果不等于 type(item) 则不会调用后面的 pipeline process_item 函数
        """
        return item

    def process_exception(self, item, exception, **kwargs):
        if isinstance(exception, Exception):
            self.logger.error(f'TestSpiderPipeline - exception: {exception}')
            return None

        return exception
```

# 持续更新中······
