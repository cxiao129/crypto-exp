import gmpy2
import binascii


# 利用Pollard p-1算法可以快速分解出p，q相差太大的n
# 适用于p-1或q-1能够被小素数整除的情况
def cald(n):
    B = 2 ** 20
    a = 2
    for i in range(2, B + 1):
        a = pow(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if (d >= 2) and (d <= (n - 1)):
            q = n // d
            n = q * d
    return d


def pollard():
    index_list = [2, 6, 19]
    plaintext = []
    for i in range(3):
        N = int(N_list[index_list[i]], 16)
        c = int(c_list[index_list[i]], 16)
        e = int(e_list[index_list[i]], 16)
        p = cald(N)
        # print("p of " + str(index_list[i]) + " is : " + str(p))
        q = N // p
        phiOfFrame = (p - 1) * (q - 1)
        d = gmpy2.invert(e, phiOfFrame)
        m = gmpy2.powmod(c, d, N)
        plaintext.append(binascii.a2b_hex(hex(m)[2:]))
    return plaintext


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
    # 使用Pollard p-1分解法爆破得出Frame2,Frame6,Frame19的模数N可在较短时间内成功分解
    plaintext2_6_19 = pollard()
    print(plaintext2_6_19)
