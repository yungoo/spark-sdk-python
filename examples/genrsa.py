# pip install cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate an RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,  # You can adjust the key size to 4096 for more security
    backend=default_backend()
)

# Get the private key in PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Get the public key from the private key
public_key = private_key.public_key()

# Get the public key in PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Print the keys
print("Private Key:")
print(private_pem.decode())

print("Public Key:")
print(public_pem.decode())
