# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), host=SANDBOX_API_HOST)

ret, info = client.get_product_stock2(proxy_type=103)
if ret is not None:
    print(ret)
    print(info)

    if ret['data'] is not None and len(ret['data']) > 0:
        product = ret['data'][1]
        ret, info = client.create_proxy(req_order_no="test008", sku=product["productId"], amount=1, duration=product["duration"],
                                        unit=product["unit"],
                                        country_code=product["countryCode"], area_code=product["areaCode"], city_code=product["cityCode"])
        print(ret)
        print(info)
        if ret is not None and ret["code"] == 200:
            ret, info = client.get_order(ret['data']["reqOrderNo"])
            print(ret)
            print(info)

assert len(ret) is not None
