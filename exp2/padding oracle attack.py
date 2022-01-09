from oracle import *
import re

C = ['9F0B13944841A832B2421B9EAF6D9836', '813EC9D944A5C8347A7CA69AA34D8DC0', 'DF70E343C4000A2AE35874CE75E64C31']

Oracle_Connect()
Message = []
Iintermediary_VALUE = []

for b in range(2):  # 对2组中间值的爆破是相同的
    Ture_IV = C[b]
    Iintermediary_value = []
    Fake_IV = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
    # 初始化Fake_IV

    padding = 1

    for i in range(15, -1, -1):  # 从中间值的最后一个字节开始爆破

        for j in range(15, i, -1):
            Fake_IV[j] = hex(int(Iintermediary_value[15 - j], 16) ^ padding)[2:].zfill(2)  # 构造IV，使后面字节均满足当前填充条件

        for n in range(256):  # 每次爆破一个字节，遍历0x00-0xFF
            Fake_IV[i] = hex(n)[2:].zfill(2)
            data = ''.join(Fake_IV) + C[b + 1]  # 拼接构造的IV和正确密文

            ctext = [(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)]
            rc = Oracle_Send(ctext, 2)

            if str(rc) == '1':  # Padding正确时, 记录Ivalue, 结束爆破
                Iintermediary_value += [hex(n ^ padding)[2:].zfill(2)]  # 逆序存储
                # print(hex(n ^ padding)[2:].zfill(2))
                break

        padding += 1

    Iintermediary_value = ''.join(Iintermediary_value[::-1])
    Iintermediary_VALUE += [Iintermediary_VALUE]

    # Ture_IV与中间值异或可以直接得到密文对应的明文，而无需密钥
    m = re.findall('[0-9a-f]+', str(hex(int(Ture_IV, 16) ^ int(Iintermediary_value, 16))))[1].decode('hex')
    Message += [m]

Oracle_Disconnect()

print('The Iintermediary_VALUE is:', ''.join(Iintermediary_VALUE))
print('The Message is:', ''.join(Message))
