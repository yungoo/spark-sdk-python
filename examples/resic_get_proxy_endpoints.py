# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# 获取订单&实例信息
ret, info = client.get_proxy_endpoints("USA")
pprint(ret)
pprint(info)
