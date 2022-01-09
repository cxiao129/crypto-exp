import gmpy2
import binascii


# 欧几里得算法
def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = gcd(b % a, a)
        return g, x - (b // a) * y, y


# 公共模数攻击
def common_modulus():
    # 寻找公共模数
    index1 = 0
    index2 = 0
    for i in range(21):
        for j in range(i + 1, 21):
            if N_list[i] == N_list[j]:
                print('Same modulus found!' + str((N_list[i], N_list[j])))
                index1, index2 = i, j
    e1 = int(e_list[index1], 16)
    e2 = int(e_list[index2], 16)
    n = int(N_list[index1], 16)
    c1 = int(c_list[index1], 16)
    c2 = int(c_list[index2], 16)
    s = gcd(e1, e2)
    s1 = s[1]
    s2 = s[2]
    # 欧几里得算法求逆元
    if s1 < 0:
        s1 = - s1
        c1 = gmpy2.invert(c1, n)
    elif s2 < 0:
        s2 = - s2
        c2 = gmpy2.invert(c2, n)

    m = pow(c1, s1, n) * pow(c2, s2, n) % n
    result = binascii.a2b_hex(hex(m)[2:])
    return result


if __name__ == "__main__":
    N_list = []
    c_list = []
    e_list = []
    for i in range(21):
        with open("frame_set/Frame" + str(i), "r") as f:
            tmp = f.read()
            N_list.append(tmp[0:256])
            e_list.append(tmp[256:512])
            c_list.append(tmp[512:768])
    # 使用公共模数攻击的方法还原出Frame0和Frame4
    plaintext0_and_4 = common_modulus()
    print(plaintext0_and_4)
