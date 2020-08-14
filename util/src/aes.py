import os
import base64

from pyaes import *

from util.src.msg import Msg


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
    aes_key = os.urandom(32)
    aes_key = base64.b64encode(aes_key).decode('utf8')

    return aes_key


def encrypt(key, data):
    aes = AESModeOfOperationCTR(base64.b64decode(key))

    cipher_text = aes.encrypt(data.encode('utf8'))
    cipher_text = base64.b64encode(cipher_text).decode('utf8')

    encrypt_msg = Msg()
    encrypt_msg.add(Msg.key_cipher_text, cipher_text)

    return encrypt_msg

def decrypt(key, encrypt_msg):
    key = base64.b64decode(key.encode('utf8'))

    cipher_text = base64.b64decode(
        encrypt_msg.data[Msg.key_cipher_text].encode('utf8'))

    aes = AESModeOfOperationCTR(key)
    data = aes.decrypt(cipher_text)

    data = data.decode()
    return data


if __name__ == '__main__':
    data = 'test string 123 ' * 5

    # key = gen_key()
    # print(f'key [{key}]')
    #
    # encrypt_msg = encrypt(key, data)
    # print(f'cipher_text [{encrypt_msg.data[Msg.key_cipher_text]}]')

    key = 'Jz0pa88iMsYoTYI2T/9EK1SEoCBCWQQOBaplzDOkv6w='
    cipher_text = 'eD7W6lJ7oJvQ22F4Ovf2jRi5Lbu2K4qIjHIxHy5c66mSAUcorWmTWgm3gt0ILlk4fuT5cBi1RFdW7mej4dAiTK3o29XAbj4wJudz5ECE4X0='

    encrypt_msg = Msg()
    encrypt_msg.add(Msg.key_cipher_text, cipher_text)

    data2 = decrypt(key, encrypt_msg)
    print(data2)
    data2 = decrypt(key, encrypt_msg)
    print(data2)
