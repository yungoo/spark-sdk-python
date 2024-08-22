# -*- coding: utf-8 -*-
# flake8: noqa
import codecs
import pprint
import time
import random

from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'spark2c'
with open("spark2c.key", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key))   #, host="http://127.0.0.1:8081")


member_id = "200000"
user_data_list = []
for i in range(0, 20):
    id = str(int(member_id) + i)
    ret, info = client.get_proxy_user(id)
    if ret['code'] == 200:
        user_info = ret["data"]
        usage = '"%s","%s","%s","%s","%s"\n' % (
            id,
            user_info['name'],
            user_info['username'],
            str(user_info['plan']),
            str(user_info['usage'])
        )
        user_data_list.append(usage)

with codecs.open('usages.txt', 'w', encoding='utf-8') as file:
    file.writelines(user_data_list)

# member_id="100015"
# name='BD大客户'
# traffic=3000   #G
#
# ret, info = client.init_proxy_user(member_id, name)
# pprint.pprint(ret)

# order_no = generate_order_id()
# ret, info = client.recharge_traffic(req_order_no=order_no, username=member_id, traffic=1000*traffic, validity_days=30)
# print(ret)
# print(info)
#
# ret, info = client.get_traffic_record(req_order_no=order_no)
# print(ret)
# print(info)


### 6.用户6mi-待开通lumi 1G美国 30条
# sp66b48f622415220446fe180a
# DgAHmztH9Syk

### 7. 用户7mi-待开通lumi 1G美国 30条
# sp66b48fb52415220446fe180b
# Ux8gFyqlRHMA

### 8. 飞翔8-待开通lumi 2G美国 30条
# sp66b48fd92415220446fe180c
# tTRZsztVkUL2

### 9. 柏树9-待开通lumi 1G美国 30条
# sp66b48ffa2415220446fe180d
# nWgbB8HXqxqj