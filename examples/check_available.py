# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read().decode("utf-8")
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read().decode("utf-8")
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key))

# 获取订单&实例信息
ret, info = client.check_available()
print(ret)
print(info)
