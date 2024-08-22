# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

ret, info = client.delete_proxy(req_order_no='17202907918472920', instances=["123e0400b9b84398910edc3dc41f91df", "6a941adce65542e6983c9b0ce23cbf8f"])
pprint(ret)
pprint(info)
