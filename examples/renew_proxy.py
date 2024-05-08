# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), host=SANDBOX_API_HOST)

# 已生效、未过期的实例，可以续费
ret, info = client.renew_proxy(req_order_no="test002", instances=[
    {"instanceId": "b32cecb6b72240eb852d78f41c82dffb", "duration": 30, "unit": 1}])

print(ret)
print(info)
