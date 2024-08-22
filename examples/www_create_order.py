# -*- coding: utf-8 -*-
# flake8: noqa
import random
import time
from pprint import pprint

from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST

supplier_no = 'spark2c'
with open("spark2c.key", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key))  #, host=DEV_API_HOST)

# req_order_no = generate_order_id()
# ret, info = client.create_proxy(req_order_no=req_order_no, sku='98aaba932bc3438f8326d5b564692a49', amount=15, duration=30,
#                                 unit=1,
#                                 country_code='USA', area_code='', city_code='', rules=[])
# pprint(ret)
# pprint(info)

# order_no_list = ["17237929398936989"]
#
# accounts = []
# # 获取订单&实例信息
# for order_no in order_no_list:
#     ret, info = client.get_order(req_order_no=order_no)
#     # pprint(ret)
#     # pprint(info)
#     for ip in ret['data']['ipInfo']:
#         p = "%s:%d:%s:%s\n" % (ip['ip'], ip['port'], ip['username'], ip['password'])
#         accounts.append(p)
#
# with open('USA-堪萨斯-15-0816.txt', 'w') as file:
#     file.writelines(accounts)
