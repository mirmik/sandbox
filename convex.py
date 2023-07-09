#!/usr/bin/env python3

import math
import sympy
import numpy

def center(X):
    V = numpy.sum(X, axis=0) / X.shape[0]
    return V

def ellipsoid(A,V,x):
    x = x - V
    return x.T @ A @ x

def ellipsoid_vec(A,V,X):
    S = []
    for i in range(X.shape[0]):
        S.append(ellipsoid(A,V,X[i]))
    return numpy.array(S)
    
def ellipsoid_fitting(X):
    V = center(X)
    S = X - V
    SS = S.T @ S
    det = numpy.linalg.det(SS)
    k=  SS / det
    A = numpy.linalg.inv(k)
    A = A / numpy.linalg.det(A)
    #metr = ellipsoid(A,V,X[0])
    #A = A / metr

    M = []
    for i in range(X.shape[0]):
        e = ellipsoid(A,V,X[i])
        M.append(e)

    A = A / numpy.max(M)

    return A, V

angle = math.pi/4
X = numpy.array([
    [0,1],
    [0.2,0.5],
    [1,0],
    [-1,0],
    [0,0.5],
    [0,2.5],
    [math.cos(math.pi/6),math.sin(math.pi/6)],
    [math.cos(math.pi/6),math.sin(math.pi/6)],
    [math.cos(angle),math.sin(angle)],
    [0,-1],
    [0,-1],
])
#print(X)


def filter_one_point(X):
    A, V = ellipsoid_fitting(X)
    M = []
    for i in range(X.shape[0]):
        M.append(ellipsoid(A,V,X[i]))
    arg = numpy.argmin(M)
    print(X, M)
    return numpy.vstack((X[:arg], X[arg+1:]))



A, V = ellipsoid_fitting(X)

print(A)
print(V)


L = ellipsoid_vec(A,V,X)
print(L)
print(L>0.4)

#F = X
#for i in range(7):
#    F = filter_one_point(F)   
#    print() 
    #print(F)

#A, V = ellipsoid_fitting(F)
#print(ellipsoid_vec(A,V,F))
#print(ellipsoid_vec(A,V,X))