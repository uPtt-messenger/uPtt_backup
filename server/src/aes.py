import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

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
    return cipher_text, tag, nonce


def decrypt(key, cipher_text, tag, nonce):
    cipher_text = base64.b64decode(cipher_text.encode('utf8'))
    key = base64.b64decode(key.encode('utf8'))
    tag = base64.b64decode(tag.encode('utf8'))
    nonce = base64.b64decode(nonce.encode('utf8'))

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(cipher_text, tag).decode('utf8')

    return data

if __name__ == '__main__':
    data = 'test string 123'

    # aes = AES()

    # key = gen_key()
    # print(f'key [{key}]')
    #
    # cipher_text, tag, nonce = encrypt(key, data)
    # print(f'cipher_text [{cipher_text}]')
    # print(f'tag [{tag}]')
    # print(f'nonce [{nonce}]')

    key = 'TPf9VIM2UkNUO3FWeRrrfSGT/GOuF0SHCMlyw2U7f9U='
    cipher_text = 'glVma7g8mnvhq5JZRoHJ'
    tag = 'ZpcE+OWzlNqylnPxmREtWA=='
    nonce = 'gRcqgW/B1n2HgZlCbjfdFg=='

    data2 = decrypt(key, cipher_text, tag, nonce)

    print(data2)

