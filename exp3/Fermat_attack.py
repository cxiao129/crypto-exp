import gmpy2
import binascii
import math


# 利用Fermat算法可以快速分解p，q相差太近的n。
def pq(n):
    B = math.factorial(2 ** 14)
    u = 0
    v = 0
    i = 0
    u0 = gmpy2.iroot(n, 2)[0] + 1
    while i <= (B - 1):
        u = (u0 + i) * (u0 + i) - n
        if gmpy2.is_square(u):
            v = gmpy2.isqrt(u)
            break
        i = i + 1
    p = u0 + i + v
    return p


def fermat_resolve():
    for i in range(10, 14):
        N = int(N_list[i], 16)
        p = pq(N)
        print(p)


def get_content_of_frame10():
    p = 9686924917554805418937638872796017160525664579857640590160320300805115443578184985934338583303180178582009591634321755204008394655858254980766008932978699
    n = int(N_list[10], 16)
    c = int(c_list[10], 16)
    e = int(e_list[10], 16)
    q = n // p
    phiOfFrame10 = (p - 1) * (q - 1)
    d = gmpy2.invert(e, phiOfFrame10)
    m = gmpy2.powmod(c, d, n)
    plaintext = binascii.a2b_hex(hex(m)[2:])
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
    # 使用费马分解法爆破，得出Frame10的模数N可在较短时间内成功分解
    fermat_resolve()
    print("Fermat finished!")
    plaintext10 = get_content_of_frame10()
    print(plaintext10)
