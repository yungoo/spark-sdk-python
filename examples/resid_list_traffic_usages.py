# -*- coding: utf-8 -*-
# flake8: noqa
from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

ret, info = client.list_traffic_usages(username="200001", start_time="2024-07-08 23:59:59", end_time="2024-07-21 23:59:59", type="days")
print(ret)
print(info)