# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST,DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

# 已生效、未过期的实例，可以续费
ret, info = client.renew_proxy(req_order_no="test002", instances=[
    {"instanceId": "de15c69d70fd48bc8f1bd28b13aaee57", "duration": 30, "unit": 1}])
pprint(ret)
pprint(info)