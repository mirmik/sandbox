#!/usr/bin/env python3
import numpy as np

# Factorize a number into its prime factors
def factorize(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n /= d
        d += 1
        if d*d > n:
            if n > 1:
                factors.append(int(n))
            break
    return np.array(factors)

list_of_primes = []
for i in range(1, 10000):
    if len(factorize(i)) == 1:
        list_of_primes.append(i)

number_of_prime = {}
for i, e in enumerate(list_of_primes):
    number_of_prime[e] = i

def is_prime(n):
    return len(factorize(n)) == 1

def vecfac(n):
    factors = factorize(n)
    res = []
    for f in factors:
        number = number_of_prime[f]
        if len(res) < number + 1:
            res += [0] * (number + 1 - len(res))
        res[number] += 1
    return np.array(res)
    
def vecfac_to_number(v):
    res = 1
    for i, e in enumerate(v):
        res *= list_of_primes[i] ** e
    return res

#for i in range(1, 100):
#    if not is_prime(i):
#        if i != 1 and vecfac(i)[0] != 1:    
#            print(i, vecfac_to_number(vecfac(i)), vecfac(i))



#for i in [4,6,12,18,30,42,60,72,102,108,138,150,180]:#,#192,198, 228, 240, 270, 282, 312, 348, 420, 432, 462, 522, 570, 600, 618, 642, 660, 810, 822, 828, 858, 882]:

for i in range(1, 10000):
    A = vecfac(i+1)
    B = vecfac(i-1)
    lenA = len(A)
    lenB = len(B)
    if lenA < lenB:
        A = np.concatenate((A, [0] * (lenB - lenA)))
    elif lenB < lenA:
        B = np.concatenate((B, [0] * (lenA - lenB)))
    print(i, A-B)

#for i in range(1, 100):
    #A = vecfac_to_number([i,1,1,1,1])
    #Apf = factorize(A+1)
    #Amf = factorize(A-1)
    #print(i, len(Apf) == 1, len(Amf) == 1, Apf, Amf)