# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from utils import generate_order_id
from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

order_no = generate_order_id()
ret, info = client.get_dynamic_area(proxy_type=104, product_id="")
pprint(ret)
pprint(info)