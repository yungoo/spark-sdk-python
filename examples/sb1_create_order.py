# -*- coding: utf-8 -*-
# flake8: noqa
from config import secret_key, supplier_no
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import DEV_API_HOST
from utils import generate_order_id

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=DEV_API_HOST)

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    print(ret)
    print(info)

    if ret['data'] is not None and len(ret['data']['products']) > 0:
        product = ret['data']['products'][1]
        ret, info = client.create_proxy(req_order_no=generate_order_id(), sku=product["productId"], amount=2, duration=product["duration"]*2,
                                        unit=product["unit"],
                                        country_code=product["countryCode"], area_code=product["areaCode"], city_code=product["cityCode"])
        print(ret)
        print(info)
        if ret is not None and ret["code"] == 200:
            ret, info = client.get_order(ret['data']["reqOrderNo"])
            print(ret)
            print(info)

assert ret is not None
