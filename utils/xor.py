import os
import math
def xor(num):
    count = 0
    num_b = bin(num)
    for i in num_b:
        if i == '1':
            count = count + 1
    if count % 2 == 0:
        num = num & 0xfe
        return num
    else:
        return num


if __name__ == '__main__':
    num = xor(1)
    print(num)