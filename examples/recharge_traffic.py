# -*- coding: utf-8 -*-
# flake8: noqa
import time
import random

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST


def generate_order_id():
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    random_num = random.randint(1000, 9999)
    order_id = "{}{}".format(timestamp, random_num)
    return order_id


supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), host="http://127.0.0.1:8081")

ret, info = client.recharge_traffic(req_order_no=generate_order_id(), username="user", traffic=1000, validity_days=90)
print(ret)
print(info)