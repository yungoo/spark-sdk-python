# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# 创建代理账号
username = "yd_200005"   # 客户方唯一用户ID

# 获取用户信息
ret, info = client.get_resi_user_info(username=username)
pprint(ret)
pprint(info)