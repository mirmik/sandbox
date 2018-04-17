#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.insert(0, "..")

import rabbit.geom2 as g2
import rabbit.topo2 as t2

pnts = [g2.vector(*t) for t in [
	(0,0),
	(33,33),
	(0,22)
]]

l1 = g2.line(pnts[0], pnts[1])
l2 = g2.line(pnts[1], pnts[2])
l3 = g2.line(pnts[2], pnts[0])


print(pnts)
print(l1.d0(10))

print(l1)
print(l2)
print(l3)