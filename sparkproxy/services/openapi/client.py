# -*- coding: utf-8 -*-
import time
import uuid

from sparkproxy import config
from sparkproxy import http


class SparkProxyClient(object):
    """资源管理客户端

    使用应用密钥生成资源管理客户端，可以进一步：
    1、部署服务和容器，获得信息
    2、创建网络资源，获得信息

    属性：
        auth: 应用密钥对，Auth对象
        host: API host

    接口：
        get_product_stock(args)
        create_proxy(args)
        renew_proxy(args)
        delete_proxy(stack)
        get_order(stack)
        get_instance(stack)
    """

    def __init__(self, auth, api_version=2, host=None):
        self.auth = auth
        self.api_version = api_version
        if host is None:
            self.host = config.get_default("default_api_host")
        else:
            self.host = host

    def __request_params(self, method, version, args):
        if self.api_version == 1:
            base_params = {
                "method": method,
                "version": version if version is not None else "2024-04-08",
                "reqId": str(uuid.uuid4()),
                "timestamp": int(time.time()),
                "supplierNo": self.auth.get_supplier_no(),
                "sign": "",
                "params": args
            }
            base_params["sign"] = self.auth.token_of_request(base_params)

            return base_params
        else:
            base_params = {"method": method, "version": version if version is not None else "2024-04-08",
                           "reqId": str(uuid.uuid4()), "timestamp": int(time.time()),
                           "supplierNo": self.auth.get_supplier_no(),
                           "params": self.auth.encrypt_request(args)}
            return base_params

    def __post(self, method, data=None, version=None):
        url = '{0}/v{1}/open/api'.format(self.host, self.api_version)
        req = self.__request_params(method, version, data)
        ret, info = http._post(url, req)
        if self.api_version > 1 and ret is not None and 'data' in ret:
            ret['data'] = self.auth.decrypt_response(ret['data'])
        return ret, info

    def get_product_stock(self, proxy_type, country_code=None, area_code=None, city_code=None):
        """获取商品库存

        列出当前所有在售的商品及其库存信息。

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回服务组列表[<product1>, <product1>, ...]，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetProductStock',
                           {"proxyType": proxy_type, "countryCode": country_code, "areaCode": area_code, "cityCode": city_code})

    def create_proxy(self, req_order_no, sku, amount, duration, unit, country_code, area_code, city_code, rules=[]):
        """创建代理实例

        创建新代理实例，返回订单信息

        Args:
            - req_order_no: 请求方订单ID
            - sku:  商品ID
            - amount: IP数量
            - duration: 必要 时长 0无限制
            - unit: 单位 1 天;2 周（7天）;3 月(自然月; 4年(自然年365，366）
            - country_code: 必要,国家代码 3位 iso标准
            - area_code: 必要,州代码 3位 iso标准
            - city_code: 必要,城市代码 向我方提取
            - rules: IP段规则数组
                - exclude bool False-not in  True-in
                - cidr string ip段，如 154.111.102.0/24
                - count int 抽取该规则段数量
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateProxy', {"reqOrderNo": req_order_no, "productId": sku, "amount": amount,
                                           "duration": duration, "unit": unit, "countryCode": country_code,
                                           "areaCode": area_code, "cityCode": city_code, "cidrBlocks": rules})

    def renew_proxy(self, req_order_no, instances):
        """续费代理实例

        续费新代理实例，返回新订单信息

        Args:
            - args:  订单&实例描述

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RenewProxy', {"reqOrderNo": req_order_no, "instances": instances})
        return ret, info

    def delete_proxy(self, req_order_no, instances):
        """删除代理实例

        删除代理实例，删除即时生效

        Args:
            - args:  实例描述

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('DelProxy', {"reqOrderNo": req_order_no, "instanceIds": instances})

    def get_order(self, req_order_no):
        """获取订单信息

        获取订单信息

        Args:
            - req_order_no:  请求方订单ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetOrder', {"reqOrderNo": req_order_no})
        if ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
            data = ret['data']
            if 'ipInfo' in data:
                for ipInfo in data['ipInfo']:
                    password = ipInfo["password"] if "password" in ipInfo else ''
                    if len(password) > 0:
                        ipInfo["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def get_instance(self, instance_id):
        """获取订单信息

        获取订单信息

        Args:
            - instance_id:  实例ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetInstance', {"instanceId": instance_id})
        if self.api_version == 1:
            if ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
                data = ret['data']
                password = data["password"] if 'password' in data else ''
                if len(password) > 0:
                    data["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def init_proxy_user(self, user_id, name):
        """获取代理用户

        获取代理用户

        Args:
            - user_id:  代理账号ID（唯一用户ID）
            - name:  账号名称

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('InitProxyUser', {"reqUserId": user_id, "name": name})
        return ret, info

    def get_proxy_user(self, username):
        """获取代理用户

        获取代理用户

        Args:
            - username:  代理账号ID（管理用户）

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetProxyUser', {"reqUserId": username})
        return ret, info

    def recharge_traffic(self, username, req_order_no, traffic, validity_days):
        """流量充值

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB
            - validity_days：有效期

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RechargeTraffic', {"reqUserId": username, "reqOrderNo": req_order_no, "traffic": traffic, "validityDays": validity_days})
        return ret, info

    def get_traffic_record(self, req_order_no):
        """获取流量充值订单信息

        Args:
            - req_order_no: 客方订单号

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetTrafficRecord', {"reqOrderNo": req_order_no})
        return ret, info

    def list_traffic_usages(self, username, start_time, end_time, type):
        """获取流量使用记录

        Args:
            - username:  关联流量账号
            - start_time: 开始时间, 可选参数, ex: 2024-05-01 00:00:00
            - end_time: 结束时间, 可选参数, ex: 2024-07-01 00:00:00
            - type: days / hours

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('ListTrafficUsage', {"reqUserId": username, "startTime": start_time, "endTime": end_time, "type": type})
        return ret, info

    def get_proxy_endpoints(self, country_code):
        """流量充值

        Args:
            - country_code:  国家代码

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetProxyEndpoints', {"countryCode": country_code})
        return ret, info

    def custom_create_proxy(self, req_order_no, ips):
        """手动创建代理账号

        Args:
            - req_order_no: 订单号
            - ips:  ip数组

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('CustomCreateProxy', {"ips": ips})
        return ret, info

    def custom_del_proxy(self, ips):
        """ 手动删除代理账号

        Args:
            - ips:  ip数组

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CustomDelProxy', {"ips": ips})

    def create_resi_user(self, username, password, status):
        """创建动态代理账号

        Args:
            - username:  客方用户ID
            - password: 密码
            - status: 1=状态 2=禁用

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateUser', {"username": username, "password": password, "status": status})

    def update_resi_user(self, username, password=None, status=None):
        """更新动态代理账号

        Args:
            - username:  客方用户ID 必填
            - password: 密码 可选
            - status: 1=状态 2=禁用 可选

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('UpdateUser', {"username": username, "password": password, "status": status})

    def get_resi_user_info(self, username):
        """获取动态代理账号

        Args:
            - username:  客方用户ID 必填

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetUserInfo', {"username": username})

    def create_resi_sub_user(self, main_username, username, password, status, usage_limit, remark):
        """创建动态代理子账号

        Args:
            - main_username 客方主账号  必填
            - username  客方子账号 必填
            - password 代理认证密码 必填
            - status 1-可用 2-禁用
            - usage_limit 可用流量 MB
            - remark 备注
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateSubUser', {"mainUsername": main_username, "username": username, "password": password,
                                             "status": status, "limitFlow": usage_limit, "remark": remark})

    def update_resi_sub_user(self, main_username, username, password=None, status=None, usage_limit=None, remark=None):
        """更新动态代理子账号

        Args:
            - main_username 客方主账号  必填
            - username  客方子账号 必填
            - password 代理认证密码 可选
            - status 1-可用 2-禁用 可选
            - usage_limit 可用流量 MB 可选
            - remark 备注 可选
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('UpdateSubUser', {"mainUsername": main_username, "username": username, "password": password,
                                             "status": status, "limitFlow": usage_limit, "remark": remark})

    def distribute_flow(self, username, req_order_no, flow):
        """分配流量

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('DistributeFlow',
                                {"username": username, "reqOrderNo": req_order_no, "flow": flow})
        return ret, info

    def recycle_flow(self, username, req_order_no, flow):
        """回收流量

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RecycleFlow',
                                {"username": username, "reqOrderNo": req_order_no, "flow": flow})
        return ret, info

    def get_dynamic_area(self, proxy_type, product_id):
        """获取动态代理地区

            Args:
                - proxy_type:  代理类型 104
                - product_id: 代理商品SKU

            Returns:
                返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
                - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                - ResponseInfo    请求的Response信息
            """
        ret, info = self.__post('GetDynamicArea',
                                {"proxyType": proxy_type, "productId": product_id})
        return ret, info

    def draw_dynamic_ips(self, username, region=None, sessTime=5, num=1, format='host:port:user:pass'):
        """获取动态代理地区

            Args:
                - username 子账号 必填
                - region IP区域 不填则全球混播
                - sessTime 会话有效期 默认5分钟
                - num 默认1
                - format 默认 host:port:user:pass

            Returns:
                返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
                - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                - ResponseInfo    请求的Response信息
            """
        ret, info = self.__post('DrawDynamicIp',
                                {"username": username, "region": region, "sessTime": sessTime, "num": num,
                                 "format": format})
        return ret, info

