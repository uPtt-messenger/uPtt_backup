import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from msg import Msg

# https://pycryptodome.readthedocs.io/en/latest/src/introduction.html
# key = get_random_bytes(32)
# cipher = AES.new(key, AES.MODE_EAX)
# ciphertext, tag = cipher.encrypt_and_digest(data.encode())
#
# cipher = AES.new(key, AES.MODE_EAX, cipher.nonce)
# data = cipher.decrypt_and_verify(ciphertext, tag).decode('utf8')
#
# print(data)


def gen_key():
    aes_key = get_random_bytes(32)
    aes_key = base64.b64encode(aes_key).decode('utf8')
    return aes_key

def encrypt(key, data):
    encrypt_cipher = AES.new(base64.b64decode(key), AES.MODE_EAX)
    cipher_text, tag = encrypt_cipher.encrypt_and_digest(data.encode())

    cipher_text = base64.b64encode(cipher_text).decode('utf8')
    tag = base64.b64encode(tag).decode('utf8')
    nonce = base64.b64encode(encrypt_cipher.nonce).decode('utf8')

    encrypt_msg = Msg()
    encrypt_msg.add(Msg.key_cipher_text, cipher_text)
    encrypt_msg.add(Msg.key_cipher_tag, tag)
    encrypt_msg.add(Msg.key_cipher_nonce, nonce)

    return encrypt_msg


def decrypt(key, encrypt_msg):
    key = base64.b64decode(key.encode('utf8'))

    cipher_text = base64.b64decode(
        encrypt_msg.data[Msg.key_cipher_text].encode('utf8'))
    tag = base64.b64decode(
        encrypt_msg.data[Msg.key_cipher_tag].encode('utf8'))
    nonce = base64.b64decode(
        encrypt_msg.data[Msg.key_cipher_nonce].encode('utf8'))

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(cipher_text, tag).decode('utf8')

    return data

if __name__ == '__main__':
    data = 'test string 123'

    key = gen_key()
    print(f'key [{key}]')

    encrypt_msg = encrypt(key, data)
    print(f'cipher_text [{encrypt_msg.data[Msg.key_cipher_text]}]')
    print(f'tag [{encrypt_msg.data[Msg.key_cipher_tag]}]')
    print(f'nonce [{encrypt_msg.data[Msg.key_cipher_nonce]}]')

    # key = 'TPf9VIM2UkNUO3FWeRrrfSGT/GOuF0SHCMlyw2U7f9U='
    # cipher_text = 'glVma7g8mnvhq5JZRoHJ'
    # tag = 'ZpcE+OWzlNqylnPxmREtWA=='
    # nonce = 'gRcqgW/B1n2HgZlCbjfdFg=='

    data2 = decrypt(key, encrypt_msg)

    print(data2)

