import gmpy2
import binascii


# 欧几里得算法
def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = gcd(b % a, a)
        return g, x - (b // a) * y, y


# e=5，低加密指数攻击
def chinese_remainder_theorem(items):
    N = 1
    for a, n in items:
        N *= n
        result = 0
    for a, n in items:
        m = N // n
        d, r, s = gcd(n, m)
        if d != 1:
            N = N // n
            continue
        result += a * s * m
    return result % N, N


def small_e_5():
    sessions = [{"c": int(c_list[3], 16), "n": int(N_list[3], 16)},
                {"c": int(c_list[8], 16), "n": int(N_list[8], 16)},
                {"c": int(c_list[12], 16), "n": int(N_list[12], 16)},
                {"c": int(c_list[16], 16), "n": int(N_list[16], 16)},
                {"c": int(c_list[20], 16), "n": int(N_list[20], 16)}]
    data = []
    for session in sessions:
        data = data + [(session['c'], session['n'])]
    x, y = chinese_remainder_theorem(data)
    # 直接开五次方根
    plaintext3_8_12_16_20 = gmpy2.iroot(gmpy2.mpz(x), 5)
    return binascii.a2b_hex(hex(plaintext3_8_12_16_20[0])[2:])


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
    # 使用低加密指数攻击的方法还原Frame3,Frame8,Frame12,Frame16,Frame20
    plaintext3_8_12_16_20 = small_e_5()
    print(plaintext3_8_12_16_20)
