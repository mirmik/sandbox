#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("..")

from gxxgeom.vector3 import *
from gxxgeom.curve import *

seg = segment(point(3,4,6), point(8,9,10))

print("seg:")
print(seg.point(0))
print(seg.point(0.25))
print(seg.point(0.5))
print(seg.point(0.75))
print(seg.point(1))

circ = elips(point(0,0,0), vector(1,0,0), vector(0,2,0))

print("circ:")
print(circ.equation(0))
print(circ.equation(math.pi / 4))
print(circ.equation(math.pi / 2))
print(circ.equation(math.pi * 3 / 4))
print(circ.equation(math.pi))
print(circ.equation(math.pi * 5 / 4))
print(circ.equation(math.pi * 3 / 2))
print(circ.equation(math.pi * 7 / 4))
print(circ.equation(2*math.pi))