# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from utils import generate_order_id
from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

ret, info = client.init_proxy_user("user", "test")
order_no = generate_order_id()
ret, info = client.recharge_traffic(req_order_no=order_no, username="user", traffic=1000, validity_days=90)
pprint(ret)
pprint(info)

ret, info = client.get_traffic_record(req_order_no=order_no)
pprint(ret)
pprint(info)