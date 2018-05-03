#!/usr/bin/env python3
#coding: utf-8

from zencad import *

drive_hole_length = 18
drive_hole_radius = 1.5
drive_hole_deep = 7.5
drive_hole2_between = 9
drive_hole2_offset = 1
hole2_x = 6
hole2_y = 3

def drive_place(t,z):
	return (
		cylinder (r = drive_hole_radius, h = t).forw(drive_hole_length/2).left(drive_hole_deep)
		+ cylinder (r = drive_hole_radius, h = t).back(drive_hole_length/2).left(drive_hole_deep)
		+ box (hole2_x,hole2_y,t,center = True).up(t/2).left(drive_hole_deep + drive_hole2_between).back(drive_hole_length/2+drive_hole2_offset)
		+ box (hole2_x,hole2_y,t,center = True).up(t/2).left(drive_hole_deep + drive_hole2_between).forw(drive_hole_length/2+drive_hole2_offset)
	)

if __name__ == "__main__":
	t = 1
	z = 20
	test_x = 25
	test_y = 30

	m = box(test_x,test_y,t).left(test_x).back(test_y/2)

	#display(m)
	display(m - drive_place(t,z))
	show()