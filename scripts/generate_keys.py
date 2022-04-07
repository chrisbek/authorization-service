import os
import rsa
from pathlib import Path


def save_key(public_key, private_key, path=f"{str(Path(os.pardir).parent.absolute())}/keys"):
    # Save the public_key
    with open(f'{path}/public.key', 'wb') as public_file:
        public_file.write(public_key.save_pkcs1())

    # Save the private_key
    with open(f'{path}/private.key', 'wb') as private_file:
        private_file.write(private_key.save_pkcs1())


def load_keys(path=f"{str(Path(os.pardir).parent.absolute())}/keys"):
    # Read the public_key
    with open(f'{path}/public.key', 'rb') as public_file:
        public_key = rsa.PublicKey.load_pkcs1(public_file.read())

    # Read the private_key
    with open(f'{path}/private.key', 'rb') as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())

    return public_key, private_key


_public_key, _private_key = rsa.newkeys(1024)
save_key(_public_key, _private_key)
print(load_keys())
