# Sparkproxy OpenApi SDK for Python

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/tag/sparkpoxy/spark-sdk-python.svg?label=release)](https://github.com/yungoo/spark-sdk-python/releases)
[![Latest Stable Version](https://img.shields.io/pypi/v/sparkproxy.svg)](https://pypi.python.org/pypi/spark-proxy)
[![Download Times](https://img.shields.io/pypi/dm/sparkproxy.svg)](https://pypi.python.org/pypi/spark-proxy)

## 安装

通过pip

```bash
$ pip install sparkproxy
```

## 运行环境

| sparkproxy SDK版本 |              Python 版本               |
|:----------------:| :------------------------------------: |
|       0.x        | 2.7, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9 |

## 使用方法

### 调用sparkproxy的开放接口

```python
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

# 双方协商的商户号
supplier_no = 'test0001'

# 使用私钥对请求签名（认证）, 生成方式参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples/genrsa.py)。
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read().decode("utf-8")
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    print('All is OK')
else:
    print(info) # error message in info
```

### 同步接口

参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples/webhooks.py)。

```python
import os
from flask import Flask, request
import time
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

# sparkproxy提供的公钥，用于验证同步接口的请求合法性
rsaPublicKey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEovKByCtmQlJJBsZzSyc97gI1
Dp62XP8SrvUPBqGlWGEKNh60n2njcUUIkMDitM2yb1vuRluu3Mzk/TvaE23JOMqA
0HPsd7IG9rNCyn7vcRXvVj1jLTVw/J+f7FJB4OzZqmOEe8kq69WCP4JIkXPvAT53
wvarJGl6cincWuZvIwIDAQAB
-----END PUBLIC KEY-----
'''

__public_key = serialization.load_pem_public_key(
    rsaPublicKey.encode(),
    backend=None  # Uses the default backend
)


def verify_signature(supplierNo, sign, reqId, timestamp):
    if not supplierNo:
        raise ValueError(f"签名参数supplierNo未提供。reqId: {reqId}")
    if not sign:
        raise ValueError(f"签名参数sign未提供。reqId: {reqId}")

    if time.time() - timestamp > 600:
        raise ValueError(f"签名已过期。reqId: {reqId}")

    str_to_sign = f"supplierNo={supplierNo}&timestamp={timestamp}"

    try:
        decoded_sign = base64.b64decode(sign)
    except Exception as e:
        raise ValueError(f"签名解码失败: {e}")

    try:
        __public_key.verify(
            decoded_sign,
            str_to_sign.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except InvalidSignature:
        raise ValueError(f"签名校验错误。reqId: {reqId}")
    except Exception as e:
        raise ValueError(f"签名验证过程中出现问题: {e}")

    return None


def verify_request(req):
    if req.is_json:
        params = req.json

        try:
            verify_signature(params['supplierNo'], params['sign'], params['timestamp'])
        except ValueError:
            return "Bad signature", 400
    else:
        return "Bad request", 400

    return None, 200


app = Flask(__name__)


@app.route("/product/sync", methods=["POST"])
def receiveSyncProducts():
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    return "", 200


@app.route("/instance/sync", methods=["POST"])
def receiveSyncInstances():
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    return "", 200


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
```


## 测试

``` bash
$ py.test
```


## 打包

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 常见问题

- 第二个参数info保留了请求响应的信息，失败情况下ret 为none, 将info可以打印出来，提交给我们。
- API 的使用 demo 可以参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples)。
- 如果碰到`ImportError: No module named requests.auth` 请安装 `requests` 。