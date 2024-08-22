# -*- coding: utf-8 -*-
# flake8: noqa
import pprint

from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST

supplier_no = 'spark2c'
with open("spark2c.key", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))   #, host=DEV_API_HOST)

order_no_list = ["17232925078526567", "17232926640359202"]

for order_no in order_no_list:
    # 获取订单&实例信息
    ret, info = client.get_order(req_order_no=order_no)
    # pprint.pprint(ret)
    # pprint(info)
    instances = []
    for ip in ret['data']['ipInfo']:
        instances.append(ip['instanceId'])
    # pprint.pprint(instances)

    ret, info = client.delete_proxy(req_order_no=order_no, instances=instances)
    print(ret)
    print(info)
