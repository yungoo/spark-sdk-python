# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from sparkproxy import SparkProxyClient, Auth
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from config import secret_key, supplier_no

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

ips=['154.3.19.152','154.3.19.112','154.3.19.185','154.3.19.193','154.3.26.63','154.3.19.223','154.3.26.38','154.3.19.200','154.3.19.44','154.3.24.246','154.3.26.143','154.3.19.202','154.3.24.191','154.3.26.78','154.3.19.75','154.3.19.229','154.3.19.250','154.3.26.48','154.3.26.160','154.3.24.166','154.3.26.179','154.3.26.161','154.3.26.165','154.3.19.212','154.3.19.218','154.3.19.176','154.3.26.159','154.3.19.37','154.3.19.140','154.3.26.129','154.3.19.180','154.3.19.205','154.3.26.98','154.3.24.172','154.3.24.196','154.3.19.151','154.3.24.253','154.3.19.169','154.3.19.186','154.3.19.144','154.3.26.225','154.3.19.109','154.3.19.148','154.3.26.221','154.3.26.210','154.3.19.81','154.3.26.105','154.3.19.248','154.3.19.107','154.3.19.170','154.3.26.241','154.3.26.162','154.3.26.102','154.3.24.175','154.3.19.246','154.3.26.180','154.3.26.72','154.3.19.241','154.3.26.149','154.3.26.89']

# ret, info = client.custom_create_proxy(generate_order_id(), ips)
# pprint.pprint(ret)
# pprint.pprint(info)

will_delete_ips = []
for ip in ips:
    if ip.startswith("154.3.19."):
        will_delete_ips.append(ip)

ret, info = client.custom_del_proxy(ips=will_delete_ips)
pprint(ret)
pprint(info)