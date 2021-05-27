# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: post_gre_sql_pool.py
    Time: 2021/4/10 下午4:49
-------------------------------------------------
    Change Activity: 2021/4/10 下午4:49
-------------------------------------------------
    Desc: 
"""
import psycopg2
from DBUtils.PooledDB import PooledDB


class PostGreHandle(object):
    __instance = {}
    __init = {}

    def __new__(cls, *args, **kwargs):
        config = kwargs['config']
        name = config.get('name', 'post_gre')

        if not cls.__instance.get(name):
            cls.__instance[name] = super().__new__(cls)

        return cls.__instance[name]

    def __init__(self, config, spider):
        name = config.get('name', 'post_gre')
        if PostGreHandle.__init.get(name):
            return
        PostGreHandle.__init[name] = True

        self.log = spider.logger
        self.config = config

        self.pool = PooledDB(
            creator=psycopg2,
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
            database=self.config['db']
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

        except Exception as e:
            self.log.info(f'sql db: {e}')
            self.log.info(f"execute failed: {sql}")
            return False

        finally:
            cur.close()
            conn.close()

    def insert_conflict_list(self, table_name, info_list, indexes=None):
        keys = list(info_list[0].keys())
        fs = ', '.join(keys)
        vs = ', '.join(list(map(lambda x: '%(' + x + ')s', keys)))

        sql = f"insert into {table_name} ({fs}) values ({vs}) on conflict ({indexes}) do nothing;"

        try:
            return self.execute(sql, info_list)
        except Exception as e:
            self.log.exception(f'insert_conflict_list.sql db: {e}')
            return False

    def insert_conflict_dict(self, table_name, info_dict, indexes=None):
        fs = ', '.join(list(info_dict.keys()))
        vs = ', '.join(list(map(lambda x: '%(' + x + ')s', [*info_dict.keys()])))
        sql = f"insert into {table_name} ({fs}) values ({vs}) on conflict ({indexes}) do nothing;"

        try:
            return self.execute(sql, info_dict)
        except Exception as e:
            self.log.exception(f'insert_conflict_dict.sql db: {e}')
            self.log.error("insert_conflict_dict.failed: " + sql + "\t" + str(info_dict.values()))
            return False

    def select(self, sql):
        conn, cur = self.get_pool()

        try:
            cur.execute(sql)
            result = cur.fetchall()

        finally:
            conn.close()
            cur.close()
        return result

    def close_pool(self):
        self.pool.close()
