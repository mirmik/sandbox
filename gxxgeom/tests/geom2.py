#!/usr/bin/env python3
#coding: utf-8

import sys
import math
sys.path.append("..")

import gxxgeom.curve2d as curve2d
import gxxgeom.base2d as base2d

l = curve2d.line2((0,1), (1,0))

print(l.d0(3))
print(l.d0(0))
print(l.d0(-1))