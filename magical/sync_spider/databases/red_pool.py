# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: red_pool.py
    Time: 2021/4/10 下午4:49
-------------------------------------------------
    Change Activity: 2021/4/10 下午4:49
-------------------------------------------------
    Desc: 
"""
import json
import redis
import copy


class RedisBase(redis.StrictRedis):
    __instance = {}
    __init = {}

    def __new__(cls, *args, **kwargs):
        config = kwargs['config']
        name = config.get('name', 'red')

        if not cls.__instance.get(name):
            cls.__instance[name] = super().__new__(cls)

        return cls.__instance[name]

    def __init__(self, config):
        name = config.get('name', 'red')
        if RedisHandler.__init.get(name):
            return
        RedisHandler.__init[name] = True

        new_config = copy.deepcopy(config)

        if new_config.get('name'):
            del new_config['name']

        super().__init__(**new_config)

    def public(self, key, msg):
        self.publish(key, msg)
        return True

    def subscribe(self, key):
        pub = self.pubsub()
        pub.subscribe(key)
        return pub

    def set_str(self, key, value, **kwargs):
        return self.set(key, value, **kwargs)

    def set_dict(self, key, value):
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        return self.set(key, value)

    def get_dict(self, key):
        data = self.get(key)
        return json.loads(data) if data else {}

    def get_list(self, key):
        data = self.get(key)
        return json.loads(data) if data else []

    def get_str(self, key):
        return self.get(key)

    def close_pool(self):
        self.connection_pool.disconnect()

    def _pipeline(self):
        pipe = self.pipeline(transaction=True)
        pipe.multi()
        return pipe


class RedisHandler(RedisBase):
    def __init__(self, config):
        super().__init__(config=config)

    def get_str(self, key):
        return self.get(key)

    def set_bit(self, table, offsets, values):
        if isinstance(offsets, list):
            if not isinstance(values, list):
                values = [values] * len(offsets)
            else:
                assert len(offsets) == len(values), "offsets值要与values值一一对应"

            pipe = self._pipeline()

            for offset, value in zip(offsets, values):
                pipe.setbit(table, offset, value)

            return pipe.execute()

        else:
            return self.setbit(table, offsets, values)

    def get_bit(self, table, offsets):
        if isinstance(offsets, list):
            pipe = self._pipeline()
            for offset in offsets:
                pipe.getbit(table, offset)

            return pipe.execute()

        else:
            return self.getbit(table, offsets)

    def bit_count(self, table):
        return self.bitcount(table)
