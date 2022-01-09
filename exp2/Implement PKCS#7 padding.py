def PCKS7_padding(text, padded_length):   # text是字符串，padded_length是分组长度
    padded_amount = 0
    if(padded_length > len(text)):
        padded_amount = padded_length - len(text) % padded_length
    padded_text = text.encode() + (chr(padded_amount) * padded_amount).encode()
    return padded_text               # 返回值是bytes类型

if __name__ == "__main__":
    input_text = "YELLOW SUBMARINE"
    print(PCKS7_padding(input_text, 20))


