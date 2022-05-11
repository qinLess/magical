# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: mysql_pool.py
    Time: 2021/4/22 上午12:41
-------------------------------------------------
    Change Activity: 2021/4/22 上午12:41
-------------------------------------------------
    Desc: 
"""
import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlHandler(object):
    __instance = {}
    __init = {}

    def __new__(cls, *args, **kwargs):
        config = kwargs['config']
        name = config.get('name', 'mysql')

        if not cls.__instance.get(name):
            cls.__instance[name] = super().__new__(cls)

        return cls.__instance[name]

    def __init__(self, config, spider):
        name = config.get('name', 'mysql')
        if MysqlHandler.__init.get(name):
            return
        MysqlHandler.__init[name] = True

        self.log = spider.logger
        self.config = config

        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=0,
            mincached=5,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['db'],
            charset=self.config['charset']
        )

    def get_pool(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def execute(self, sql, info_data=None):
        conn, cur = self.get_pool()
        try:
            if isinstance(info_data, dict):
                cur.execute(sql, info_data)
            elif isinstance(info_data, list):
                cur.executemany(sql, info_data)
            else:
                cur.execute(sql)
            conn.commit()
            return True

        except pymysql.err.IntegrityError as e:
            self.log.info(f'pymysql.err.IntegrityError: {e}')
            self.log.info(f"execute failed: {sql}")
            return False

        except Exception as e:
            self.log.info(f'mysql db: {e}')
            self.log.info(f"execute failed: {sql}")
            return False

        finally:
            cur.close()
            conn.close()

    def insert_dict(self, table_name, info_dict, ignore=False, replace=False):
        fs = ','.join(list(map(lambda x: '`' + x + '`', [*info_dict.keys()])))
        vs = ','.join(list(map(lambda x: '%(' + x + ')s', [*info_dict.keys()])))

        sql = f"insert into `{table_name}` ({fs}) values ({vs});"
        if ignore:
            sql = f"insert ignore into `{table_name}` ({fs}) values ({vs});"
        elif replace:
            sql = f"replace into {table_name} ({fs}) values ({vs});"

        try:
            return self.execute(sql, info_dict)

        except Exception as e:
            self.log.info(f'insert_dict.mysql db: {e}')
            self.log.info("insert_dict.failed: " + sql + "\t" + str(info_dict.values()))

    def insert_list(self, table_name, info_list, ignore=False, replace=False):
        keys = list(info_list[0].keys())
        fs = ', '.join(keys)
        vs = ', '.join(list(map(lambda x: '%(' + x + ')s', keys)))

        sql = f"insert into {table_name} ({fs}) values ({vs});"
        if ignore:
            sql = f"insert ignore into {table_name} ({fs}) values ({vs});"
        elif replace:
            sql = f"replace into {table_name} ({fs}) values ({vs});"

        try:
            return self.execute(sql, info_list)
        except Exception as e:
            self.log.info(f'insert_list.mysql db: {e}')

    def select(self, sql):
        conn, cur = self.get_pool()
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
        cur.close()
        return result

    def close_pool(self):
        self.pool.close()
