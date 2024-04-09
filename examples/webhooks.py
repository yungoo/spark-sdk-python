import os
from flask import Flask, request
import time
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

webhook_secret = os.environ.get("WEBHOOK_SECRET")

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
