import binascii

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


# 兼容Python 2和3的编码函数
def to_bytes(data, encoding='utf-8'):
    if isinstance(data, str):
        return data.encode(encoding)
    return data


def to_string(data, encoding='utf-8'):
    """
    将数据转换为字符串。

    Args:
        data: 要转换的数据。
        encoding: 字符串编码。

    Returns:
        str: 转换后的字符串。
    """
    if isinstance(data, bytes):
        return data.decode(encoding)
    elif isinstance(data, str):
        return data
    else:
        return str(data)


# 兼容Python 2和3的十六进制解码函数
def from_hex(s):
    try:
        return bytes.fromhex(s)  # Python 3
    except AttributeError:
        return s.decode('hex')  # Python 2


# 兼容Python 2和3的十六进制编码函数
def to_hex(data):
    try:
        return data.hex()  # Python 3
    except AttributeError:
        return binascii.hexlify(data)  # Python 2


def rsa_load_pem_private_key(pri_key):
    private_key = serialization.load_pem_private_key(
        to_bytes(pri_key),
        password=None,
        backend=default_backend()
    )
    return private_key


def rsa_load_pem_public_key(pub_key):
    public_key = serialization.load_pem_public_key(
        to_bytes(pub_key),
        backend=default_backend()  # 显式指定后端
    )
    return public_key


def rsa_public_encrypt(msg, public_key):
    decoded_msg = to_bytes(msg)

    encrypted_msg = public_key.encrypt(
        decoded_msg,
        padding.PKCS1v15()
    )

    return to_hex(encrypted_msg)


def rsa_private_decrypt(encrypted_msg_hex, private_key):
    encrypted_msg = from_hex(encrypted_msg_hex)

    decrypted_msg = private_key.decrypt(
        encrypted_msg,
        padding.PKCS1v15()
    )

    return decrypted_msg


def rsa_sign(message, private_key):
    signature = private_key.sign(
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return to_hex(signature)


def rsa_verify(sign, message, public_key):
    try:
        decoded_sign = from_hex(sign)
    except Exception as e:
        raise ValueError("签名解码失败: {}".format(e))

    public_key.verify(
        decoded_sign,
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
