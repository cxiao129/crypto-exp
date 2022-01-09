import gmpy2
import binascii


# 因数碰撞法
def common_factor():
    plaintext = []
    index = []
    for i in range(21):
        for j in range(i + 1, 21):
            if int(N_list[i], 16) == int(N_list[j], 16):
                continue
            prime = gmpy2.gcd(int(N_list[i], 16), int(N_list[j], 16))
            if prime != 1:
                print((N_list[i], N_list[j]))
                print((i, j))
                index.append(i)
                index.append(j)
                pOfFrame = prime
    qOfFrame1 = int(N_list[index[0]], 16) // pOfFrame
    qOfFrame18 = int(N_list[index[1]], 16) // pOfFrame
    print(pOfFrame)
    print(qOfFrame1, qOfFrame18)

    phiOfFrame1 = (pOfFrame - 1) * (qOfFrame1 - 1)
    phiOfFrame18 = (pOfFrame - 1) * (qOfFrame18 - 1)
    dOfFrame1 = gmpy2.invert(int(e_list[index[0]], 16), phiOfFrame1)
    dOfFrame18 = gmpy2.invert(int(e_list[index[1]], 16), phiOfFrame18)

    plaintextOfFrame1 = gmpy2.powmod(int(c_list[index[0]], 16), dOfFrame1, int(N_list[index[0]], 16))
    plaintextOfFrame18 = gmpy2.powmod(int(c_list[index[1]], 16), dOfFrame18, int(N_list[index[1]], 16))
    plaintextOfFrame1 = binascii.a2b_hex(hex(plaintextOfFrame1)[2:])
    plaintextOfFrame18 = binascii.a2b_hex(hex(plaintextOfFrame18)[2:])

    plaintext.append(plaintextOfFrame1)
    plaintext.append(plaintextOfFrame18)
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
    # 使用因数碰撞法还原出Frame1和Frame18
    plaintext1_and_18 = common_factor()
    print(plaintext1_and_18)        