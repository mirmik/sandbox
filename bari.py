#!/usr/bin/env python3

import numpy

numpy.set_printoptions(precision=4, suppress=True)

A = numpy.array([
    [0,1,0,0.6,1],
    [0,0,1,1.6,1],
    [1,1,1,1,1]
])


b = numpy.array([
    [1],
    [3],
    [1]
])


AAT_betta = A.T @ A #- 0 * numpy.diag([1,1,1,1])
ATb = A.T @ b

print(AAT_betta)
AI = numpy.linalg.pinv(AAT_betta)
print(AI)


s = numpy.sum(AI, axis=1)
r = numpy.sum(AI, axis=0)

print()
print(s)
print(r)
#print(numpy.linalg.pinv(A))