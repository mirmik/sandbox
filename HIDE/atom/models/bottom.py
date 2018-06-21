#!/usr/bin/env python3
#coding: utf-8

from zencad import *

enable_cache(".bottom_cache")

x = 100
y = 150
z = 5
t = 1.5

s = y/4


m =  difference([
	linear_extrude(rectangle(x, y, center = True).fillet(5,[0,1,2,3]),(0,0,z)),
	linear_extrude(rectangle(x-2*t, y-2*t, center = True).fillet(5-t,[0,1,2,3]),(0,0,z-t)).up(t)
])

drive_place = (box(t,d,z, center = True).up(z/2) 
	+ cylinder (r = drive_hole_radius, h = t).forw(drive_hole_length/2).left(drive_hole_deep)
	+ cylinder (r = drive_hole_radius, h = t).back(drive_hole_length/2).left(drive_hole_deep)
)

m = difference ([m,
	drive_place.right(x/2-t/2).forw(s),
	drive_place.right(x/2-t/2).back(s),
	drive_place.mirrorYZ().left(x/2-t/2).forw(s),
	drive_place.mirrorYZ().left(x/2-t/2).back(s),
]) 

display(m)
show()