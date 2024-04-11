import os

from flask import Flask, request

from sparkproxy import Auth

# sparkproxy提供的公钥，用于验证同步接口的请求合法性
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()

supplier_no = 'test0001'
auth = Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key)


def verify_request(req):
    if req.is_json:
        params = req.json

        try:
            auth.verify_callback(params['supplierNo'], params['sign'], params['reqId'], params['timestamp'])
        except ValueError:
            return "Bad signature", 400
    else:
        return "Bad request", 400

    return None, 200


app = Flask(__name__)


@app.route("/checkAvailable", methods=["POST"])
def receiveCheckAvailable():
    # 验签
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    # 取出参数字符串，把16进制字符串转为二进制
    cyper_text = request.json["data"]

    # 通过自己的私钥解密
    plain_text = auth.decrypt_using_private_key(cyper_text)

    # 把解密字符串用对方的公钥加密，并转为16进制字符串
    new_cyper_text = auth.encrypt_using_remote_public_key(plain_text)

    return {
        "code": 200,
        "msg": "ok",
        "data": new_cyper_text
    }


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

    ret = request.json
    if ret is not None:
        for ipInfo in ret['data']['ipInfo']:
            password = ipInfo["password"]
            if len(password) > 0:
                ipInfo["password"] = auth.decrypt_using_private_key(password)

    print(ret)

    return "", 200


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
