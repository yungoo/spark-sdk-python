# -*- coding: utf-8 -*-
import random
import time


def generate_order_id():
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    random_num = random.randint(1000, 9999)
    order_id = "{}{}".format(timestamp, random_num)
    return order_id