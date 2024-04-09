# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read().decode("utf-8")

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))

# 已生效、未过期的实例，可以续费
ret, info = client.delete_proxy(req_order_no="test002", instances=["b32cecb6b72240eb852d78f41c82dffb"])

print(ret)
print(info)
