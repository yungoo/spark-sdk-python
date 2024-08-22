# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# 获取订单&实例信息
userId = "200005"
ret, info = client.init_proxy_user(userId, "jp-2g-new")
pprint(ret)
pprint(info)