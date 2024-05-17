# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), host=SANDBOX_API_HOST)
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))

ret, info = client.get_product_stock2(proxy_type=103)
if ret is not None and ret['code'] == 200:
    print(ret)
    print(info)
    # 去掉了skus，相关属性提到product里
    assert len(ret['data'][0]['countryCode']) > 0
