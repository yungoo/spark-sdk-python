# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from utils import generate_order_id
from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

username = "yd_200005"   # 客户方唯一用户ID

order_no = generate_order_id()
ret, info = client.distribute_flow(req_order_no=order_no, username=username, flow=1024)
pprint(ret)
pprint(info)