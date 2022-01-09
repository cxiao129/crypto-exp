import random
import os
from Crypto.Cipher import AES


def PCKS7_padding(text: bytes, padded_length: int) -> bytes:
    padded_amount = padded_length - len(text) % padded_length
    padded_text = text + (chr(padded_amount) * padded_amount).encode()
    return padded_text


def AES_ECB_encrypt(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)


def AES_CBC_encrypt(plaintext: bytes, IV: bytes, key: bytes) -> bytes:
    previous = IV
    keysize = len(key)
    ciphertext = b""
    xored = b""
    cipher = ""

    for i in range(0, len(plaintext), keysize):
        xor_list = [(b1 ^ b2).to_bytes(1, "big") for b1, b2 in zip(plaintext[i:i + keysize], previous)]
        # 不能使用encode(),异或后可能超出0x7f,utf-8编码后用两个字节表示,应该将10进制整数直接转换成相应的16进制数
        xored = b"".join(xor_list)
        cipher = AES_ECB_encrypt(xored, key)
        ciphertext += cipher
        previous = cipher  # 保留前一个密文的副本

    return ciphertext


# ECB模式加密，相同的16字节明文块总是生成相同的16字节密文块
def detect_AES_ECB(ciphertext: bytes) -> bool:
    detects = []
    for i in range(0, len(ciphertext), 16):
        detects.append(ciphertext[i:i + 16])
    for block in detects:
        if detects.count(block) > 1:
            return True
    return False


# 随机16字节密钥
key = os.urandom(16)

text = open("11.txt").read()

# 在明文前和明文后添加5到10随机字节
plaintext = os.urandom(random.randint(5, 10))
plaintext += text.encode()
plaintext += os.urandom(random.randint(5, 10))

# 填充
plaintext_padded = PCKS7_padding(plaintext, len(key))

flag = random.randint(0, 1)
if flag == 1:
    print("Encrypting using AES_ECB Encryption.")
    ciphertext = AES_ECB_encrypt(plaintext_padded, key)
else:
    print("Encrypting using AES_CBC Encryption.")
    ciphertext = AES_CBC_encrypt(plaintext_padded, os.urandom(16), key)

if detect_AES_ECB(ciphertext):
    print("Ciphertext is AES_ECB encrypted.")
else:
    print("Ciphertext is AES_CBC encrypted.")
