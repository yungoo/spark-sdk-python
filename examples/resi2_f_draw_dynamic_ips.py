# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from utils import generate_order_id
from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

username = "yd_200005_02"
region="usa"
sessTime=None
num=100
format="user:pass@host:port"
ret, info = client.draw_dynamic_ips(username=username, region=region, sessTime=sessTime, num=num, format=format)
pprint(ret)
pprint(info)