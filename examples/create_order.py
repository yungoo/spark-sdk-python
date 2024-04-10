# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    print(ret)
    print(info)

    if len(ret['data']) > 0 and len(ret['data'][0]["skus"]) > 0:
        product = ret['data'][0]
        sku = product["skus"][0]
        ret, info = client.create_proxy(req_order_no="test001", sku=sku["sku"], amount=1, duration=sku["duration"],
                                        unit=sku["unit"],
                                        country_code=product["countryCode"], city_code=product["cityCode"])
        print(ret)
        print(info)
        if ret is not None:
            ret, info = client.get_order(ret['data']["reqOrderNo"])
            print(ret)
            print(info)

assert len(ret) is not None
