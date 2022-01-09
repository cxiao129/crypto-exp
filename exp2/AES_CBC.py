from Crypto.Cipher import AES


def PKCS7_pad(plaintext: bytes, block_size: int) -> bytes:
    """
    Pad the given text upto the length of given block_size following PKCS7 norms.
    """
    if len(plaintext) == block_size:
        return plaintext
    pad = block_size - len(plaintext) % block_size
    plaintext += (pad.to_bytes(1, "big")) * pad
    return plaintext


def PKCS7_padded(text: bytes) -> bool:
    """
    Checks if the given text is padded according to the PKCS7 norms.
    """
    padding = text[-text[-1]:]

    # Check that all the bytes in the range indicated by the padding are equal to the padding value itself.
    return all(padding[b] == len(padding) for b in range(0, len(padding)))


def AES_ECB_decrypt(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(plaintext)


def PKCS7_unpad(paddedtext: bytes) -> bytes:
    """
    Unpads the given text if it's padded according to PKCS7 norms.
    """

    # Checks if the text is padded according to PKCS7 norms.
    if PKCS7_padded(paddedtext):
        # The last byte is a padding byte.
        pad_Length = paddedtext[len(paddedtext) - 1]
        # Returns the text uptil last "pad" length bytes since pad byte value is the same as number of pad bytes required.
        return paddedtext[:-pad_Length]
    else:
        return paddedtext


def AES_CBC_decrypt(ciphertext: bytes, IV: bytes, key: bytes) -> bytes:
    previous = IV
    keysize = len(key)
    plaintext = b""
    cipher = ""

    for i in range(0, len(ciphertext), keysize):
        cipher = AES_ECB_decrypt(ciphertext[i:i + keysize], key)
        xor_list = [chr(b1 ^ b2) for b1, b2 in zip(cipher, previous)]
        plaintext += "".join(xor_list).encode()
        previous = ciphertext[i:i + keysize]

    return plaintext


def AES_ECB_encrypt(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    text = PKCS7_pad(plaintext, len(key))
    return cipher.encrypt(PKCS7_pad(text, len(key)))


def AES_CBC_encrypt(plaintext: bytes, IV: bytes, key: bytes) -> bytes:
    previous = IV
    keysize = len(key)
    ciphertext = b""
    xored = b""

    for i in range(0, len(plaintext), keysize):
        xor_list = [(b1 ^ b2).to_bytes(1, "big") for b1, b2 in
                    zip(PKCS7_pad(plaintext[i:i + keysize], keysize), previous)]
        xored = b"".join(xor_list)
        cipher = AES_ECB_encrypt(xored, key)
        ciphertext += cipher
        previous = cipher

    return ciphertext
