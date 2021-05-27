# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: bloom_filter.py
    Time: 2021/5/13 下午3:31
-------------------------------------------------
    Change Activity: 2021/5/13 下午3:31
-------------------------------------------------
    Desc: 
"""
import hashlib
import math
import threading
import time

from struct import unpack, pack

from magical.sync_spider.middleware.duplicate import bit_array
from magical.sync_spider.common.redis_lock import RedisLock


def make_hash_funcs(num_slices, num_bits):
    if num_bits >= (1 << 31):
        fmt_code, chunk_size = "Q", 8
    elif num_bits >= (1 << 15):
        fmt_code, chunk_size = "I", 4
    else:
        fmt_code, chunk_size = "H", 2
    total_hash_bits = 8 * num_slices * chunk_size
    if total_hash_bits > 384:
        hash_fn = hashlib.sha512
    elif total_hash_bits > 256:
        hash_fn = hashlib.sha384
    elif total_hash_bits > 160:
        hash_fn = hashlib.sha256
    elif total_hash_bits > 128:
        hash_fn = hashlib.sha1
    else:
        hash_fn = hashlib.md5

    fmt = fmt_code * (hash_fn().digest_size // chunk_size)
    num_salts, extra = divmod(num_slices, len(fmt))
    if extra:
        num_salts += 1
    salts = tuple(hash_fn(hash_fn(pack("I", i)).digest()) for i in range(num_salts))

    def _make_hash_funcs(key):
        if isinstance(key, str):
            key = key.encode("utf-8")
        else:
            key = str(key).encode("utf-8")

        i = 0
        for salt in salts:
            h = salt.copy()
            h.update(key)
            for uint in unpack(fmt, h.digest()):
                yield uint % num_bits
                i += 1
                if i >= num_slices:
                    return

    return _make_hash_funcs


class BloomFilter(object):
    def __init__(self, spider, filter_queue_type):
        self.capacity = spider.settings.get_int('FILTER_INITIAL_CAPACITY')
        self.error_rate = spider.settings.get_float('FILTER_ERROR_RATE')

        if not (0 < self.error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")

        if not self.capacity > 0:
            raise ValueError("Capacity must be > 0")

        num_slices = int(math.ceil(math.log(1.0 / self.error_rate, 2)))
        bits_per_slice = int(
            math.ceil(
                (self.capacity * abs(math.log(self.error_rate)))
                / (num_slices * (math.log(2) ** 2))
            )
        )

        self.num_slices = num_slices
        self.bits_per_slice = bits_per_slice
        self.num_bits = num_slices * bits_per_slice
        self.make_hashes = make_hash_funcs(self.num_slices, self.bits_per_slice)

        self._is_at_capacity = False
        self._check_capacity_time = 0

        if filter_queue_type == 'memory':
            self.bit_array = bit_array.MemoryBitArray(self.num_bits)
            self.bit_array.set_all(False)

        elif filter_queue_type == 'redis':
            self.bit_array = bit_array.RedisBitArray(spider)

        else:
            raise ValueError("not support this filter_queue_type")

    def is_at_capacity(self, filter_key):
        if self._is_at_capacity:
            return self._is_at_capacity

        bit_count = self.bit_array.count(filter_key)
        if bit_count and bit_count / self.num_bits > 0.5:
            self._is_at_capacity = True

        return self._is_at_capacity

    def get(self, filter_key, value):
        is_list = isinstance(value, list)
        keys = value if is_list else [value]
        is_exists = []

        offsets = []
        for key in keys:
            hashes = self.make_hashes(key)
            offset = 0
            for k in hashes:
                offsets.append(offset + k)
                offset += self.bits_per_slice

        old_values = self.bit_array.get(filter_key, offsets)

        for i in range(0, len(old_values), self.num_slices):
            is_exists.append(int(all(old_values[i: i + self.num_slices])))

        return is_exists if is_list else is_exists[0]

    def add(self, filter_key, value):
        if self.is_at_capacity(filter_key):
            raise IndexError("BloomFilter is at capacity")

        is_list = isinstance(value, list)
        keys = value if is_list else [value]
        is_added = []

        offsets = []
        for key in keys:
            hashes = self.make_hashes(key)
            offset = 0
            for k in hashes:
                offsets.append(offset + k)
                offset += self.bits_per_slice

        old_values = self.bit_array.set(filter_key, offsets, 1)
        for i in range(0, len(old_values), self.num_slices):
            is_added.append(1 ^ int(all(old_values[i: i + self.num_slices])))

        return is_added if is_list else is_added[0]


class ScalableBloomFilter(object):
    def __init__(self, spider):
        self.spider = spider
        red_name = spider.settings['FILTER_REDIS_NAME']
        self.red = getattr(spider, red_name) if not red_name else spider.red

        self.filter_queue_type = spider.settings['FILTER_QUEUE_TYPE']

        self.filters = []
        self.filters.append(self.create_filter())

        self._thread_lock = threading.RLock()
        self._check_capacity_time = 0

    def create_filter(self):
        return BloomFilter(self.spider, self.filter_queue_type)

    def __check_filter_capacity(self, filter_key):
        if not self._check_capacity_time or time.time() - self._check_capacity_time > 1800:
            if self.filter_queue_type == 'memory':
                with self._thread_lock:
                    while True:
                        if self.filters[-1].is_at_capacity(filter_key):
                            self.filters.append(self.create_filter())
                        else:
                            break

                    self._check_capacity_time = time.time()
            else:
                # 全局锁 同一时间只有一个进程在真正的创建新的filter，等这个进程创建完，其他进程只是把刚创建的filter append进来
                with RedisLock(key="ScalableBloomFilter", timeout=300, wait_timeout=300, redis_cli=self.red) as lock:
                    if lock.locked:
                        while True:
                            if self.filters[-1].is_at_capacity(filter_key):
                                self.filters.append(self.create_filter())
                            else:
                                break

                        self._check_capacity_time = time.time()

    def get(self, filter_key, value):
        self.__check_filter_capacity(filter_key)

        is_list = isinstance(value, list)
        keys = value if is_list else [value]
        not_exist_keys = list(set(keys))

        # 检查之前的bloomFilter是否存在
        # 记录下每级filter存在的key，不存在的key继续向下检查
        for f in reversed(self.filters):
            # 当前的filter是否存在
            current_filter_is_exists = f.get(filter_key, not_exist_keys)

            not_exist_keys_temp = []

            for checked_key, is_exist in zip(not_exist_keys, current_filter_is_exists):
                # 当前filter不存在的key 需要继续向下检查
                if not is_exist:
                    not_exist_keys_temp.append(checked_key)

            not_exist_keys = not_exist_keys_temp

            if not not_exist_keys:
                break

        # 比较key是否已存在, 内部重复的key 若不存在啊则只留其一算为不存在，其他看作已存在
        for i, key in enumerate(keys):
            for j, not_exist_key in enumerate(not_exist_keys):
                if key == not_exist_key:
                    keys[i] = 0
                    not_exist_keys.pop(j)
                    break
            else:
                keys[i] = 1

        is_exists = keys
        return is_exists if is_list else is_exists[0]

    def add(self, filter_key, value, skip_check=False):
        self.__check_filter_capacity(filter_key)

        current_filter = self.filters[-1]

        if skip_check:
            return current_filter.add(filter_key, value)

        else:
            is_list = isinstance(value, list)
            keys = value if is_list else [value]
            not_exist_keys = list(set(keys))

            # 检查之前的bloomFilter是否存在
            # 记录下每级filter存在的key，不存在的key继续向下检查
            for f in reversed(self.filters):
                # 当前的filter是否存在
                current_filter_is_exists = f.get(filter_key, not_exist_keys)

                not_exist_keys_temp = []

                for key, is_exist in zip(not_exist_keys, current_filter_is_exists):
                    # 当前filter不存在的key 需要继续向下检查
                    if not is_exist:
                        not_exist_keys_temp.append(key)

                not_exist_keys = not_exist_keys_temp

                if not not_exist_keys:
                    break

            # 仍有不存在的关键词，记录该关键词
            if not_exist_keys:
                current_filter.add(filter_key, not_exist_keys)

            # 比较key是否已存在, 内部重复的key 若不存在啊则只留其一算为不存在，其他看作已存在
            for i, key in enumerate(keys):
                for j, not_exist_key in enumerate(not_exist_keys):
                    if key == not_exist_key:
                        keys[i] = 1
                        not_exist_keys.pop(j)
                        break
                else:
                    keys[i] = 0

            is_added = keys
            return is_added if is_list else is_added[0]

    @property
    def capacity(self):
        return sum(f.capacity for f in self.filters)
