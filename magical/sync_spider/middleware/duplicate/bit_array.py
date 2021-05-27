# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: bit_array.py
    Time: 2021/5/13 下午3:45
-------------------------------------------------
    Change Activity: 2021/5/13 下午3:45
-------------------------------------------------
    Desc: 
"""
from __future__ import absolute_import

import bitarray


class BitArray:
    def set_all(self, value):
        pass

    def set(self, key, offsets, values):
        raise ImportError("this method mush be implement")

    def get(self, key, offsets):
        raise ImportError("this method mush be implement")

    def count(self, key, value=True):
        raise ImportError("this method mush be implement")


class MemoryBitArray(BitArray):
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bit_array = bitarray.bitarray(num_bits, endian="little")

        self.set_all(0)

    def set_all(self, value):
        self.bit_array.setall(value)

    def set(self, key, offsets, values):
        old_values = []

        if isinstance(offsets, list):
            if not isinstance(values, list):
                values = [values] * len(offsets)
            else:
                assert len(offsets) == len(values), "offsets值要与values值一一对应"

            for offset, value in zip(offsets, values):
                old_values.append(int(self.bit_array[offset]))
                self.bit_array[offset] = value

        else:
            old_values = int(self.bit_array[offsets])
            self.bit_array[offsets] = values

        return old_values

    def get(self, key, offsets):
        if isinstance(offsets, list):
            return [self.bit_array[offset] for offset in offsets]
        else:
            return self.bit_array[offsets]

    def count(self, key, value=True):
        return self.bit_array.count(value)


class RedisBitArray(BitArray):
    redis_db = None

    def __init__(self, spider):
        red_name = spider.settings['FILTER_REDIS_NAME']
        self.red = getattr(spider, red_name) if not red_name else spider.red

        self.count_cached_name = "{}_count_cached"

    def set(self, key, offsets, values):
        return self.red.set_bit(key, offsets, values)

    def get(self, key, offsets):
        return self.red.get_bit(key, offsets)

    def count(self, key, value=True):
        # 先查redis的缓存，若没有 在统计数量
        count = self.red.get_str(self.count_cached_name)
        if count:
            return int(count)
        else:
            count = self.red.bit_count(key)
            # 半小时过期
            self.red.set_str(self.count_cached_name.format(key), count, ex=1800)
            return count
