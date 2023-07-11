#!/usr/bin/env python3

import math

# ARR = [4, 3, 1, 4, 1, 2]
# CUR = [0, 0, 0, 0, 0, 0]
ARR = [4, 3, 2, 2]
CUR = [0] * len(ARR)


def rec(level, current, target):
    rets = 0
    # print(level, current)

    if current == target:
        return 1

    for i in range(len(ARR)):
        cur = list(current)
        is_last = cur[i] == 0
        cur[i] += 1
        if cur[i] <= target[i]:
            rets += rec(level+1, cur, target)
        if is_last:
            break
    return rets


print(rec(0, CUR, ARR))
A = math.comb(2+2-1, 2-1)
B = math.comb(2+2+3-1, 3-1) * A
C = math.comb(2+2+3+4-1, 4-1) * B
print(A)
print(B)
print(C)


print(math.factorial(2+2+3-1) * math.factorial(2+2-1) / math.factorial(2) /
      math.factorial(4) / math.factorial(2))
