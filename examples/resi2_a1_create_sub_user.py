# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# 创建代理账号
main_username = "yd_200005"   # 客户方唯一用户ID
username = "yd_200005_01"   # 客户方唯一用户ID
password = "1234"
usage_limit = 5 * 1024  # MB
status = 1  # 1-可用 2-禁用
remark = '测试用户1'

# Case-1: 正常，重复创建返回"子账号已存在"(10061)
ret, info = client.create_resi_sub_user(main_username=main_username, username=username, password=password,
                                        status=status, usage_limit=usage_limit, remark=remark)
pprint(ret)
pprint(info)

# Case-2: 主账号不存在 10052
ret, info = client.create_resi_sub_user(main_username="yd_1", username=username, password=password,
                                        status=status, usage_limit=usage_limit, remark=remark)
pprint(ret)
pprint(info)