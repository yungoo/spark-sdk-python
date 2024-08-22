# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST,DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# supplier_no = 'test0001'
# with open("key.pem", 'rb') as pem_file:
#     private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=DEV_API_HOST)


# 获取订单&实例信息
ret, info = client.get_order(req_order_no="676671930442128_USA_1_1712766719.7079542")
pprint(ret)
pprint(info)

# 主动获取实例信息
ret, info = client.get_instance(instance_id="c171228a1bdb479ca9023b1e49ac377a")
pprint(ret)
pprint(info)

