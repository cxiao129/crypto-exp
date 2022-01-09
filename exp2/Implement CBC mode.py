import base64
from Crypto.Cipher import AES

f = open('10.txt', mode='r', encoding='utf-8')
b64_data = f.readlines()
f.close()

key = b"YELLOW SUBMARINE"  # 128bit的密钥

# 检查是否存在PKCS#7填充
def PKCS7_padding_check(text: bytes) -> bool:
    padding = text[-text[-1]:]  # 填充字节数等于被填充字节的值
    return all(padding[b] == len(padding) for b in range(0, len(padding)))


# 去除PKCS#7填充（考虑dummy block）
def PKCS7_unpad(padded_text: bytes) -> bytes:
    # 检查是否存在填充
    if PKCS7_padding_check(padded_text):
        # 去除末尾填充，若为dummy block，则全部清空
        return padded_text[:len(padded_text) - padded_text[-1]]
    else:
        print("未按PKCS#7标准填充!")
        exit()


def AES_CBC_decrypt(ciphertext: bytes, IV: bytes, key: bytes) -> bytes:
    previous = IV
    keysize = len(key)  # 16字节
    plaintext = b""
    cipher = ""
    model = AES.MODE_ECB  # 定义ECB模式
    aes = AES.new(key, model)  # 创建一个aes对象
    for i in range(0, len(ciphertext), keysize):
        cipher = aes.decrypt(ciphertext[i:i + keysize])  # 分组进行ECB解密
        xor_list = [(b1 ^ b2).to_bytes(1, "big") for b1, b2 in zip(cipher, previous)]  # 解密的结果和前一个密文按字节异或
        plaintext = plaintext + b"".join(xor_list)  # 明文顺序连接
        previous = ciphertext[i:i + keysize]  # 保留前一个密文的副本
    return plaintext


ciphertext = b"".join([base64.b64decode(line.strip()) for line in b64_data])  # base64解码
plaintext = PKCS7_unpad(AES_CBC_decrypt(ciphertext, b'\x00' * 16, key))  # 解密得到明文，再去除填充
print(plaintext.decode("utf-8").strip('\n'))
