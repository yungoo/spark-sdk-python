# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))

# 获取订单&实例信息
ret, info = client.get_order(req_order_no="test001")
print(ret)
print(info)

# 主动获取实例信息
ret, info = client.get_instance(instance_id="b32cecb6b72240eb852d78f41c82dffb")
print(ret)
print(info)

