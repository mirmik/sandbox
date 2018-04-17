#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("..")

from gxxgeom.curve import *
from gxxgeom.gui import *
from gxxgeom.monitor import *
from gxxgeom.render import *

monitor = Monitor(1000, 1000)
scene = Scene()
camera = Camera(scene, monitor)
render = Render()

q = gxxgeom.base.quaternion()

def updateData():
	monitor.clear()
	render.display(camera, monitor)
	gui.setData(monitor.array)

def mouseEvent(diff):
	global q
	if diff.x() != 0:
		camera.xevent(diff.x())
	
	if diff.y() != 0:
		camera.yevent(diff.y())

def wheelEvent(angle):
	camera.zevent(angle)

def centerEvent(diff):
	if diff.x() != 0:
		camera.xstrfevent(diff.x())
	
	if diff.y() != 0:
		camera.ystrfevent(diff.y())
	
gui = GUI()
updateData()
gui.setTimeoutHandler(updateData)
gui.connectMouseHandler(mouseEvent)
gui.connectWheelHandler(wheelEvent)
gui.connectCenterHandler(centerEvent)

def zhandler():
	#camera.quaternion = gxxgeom.base.quaternion(1, 0, 0, 0)
	camera.yaw = -1
	camera.pitch = -1.3
	camera.scale = 1

def xhandler():
	camera.quaternion = gxxgeom.base.quaternion(0.71, 0.71, 0, 0)

def chandler():
	camera.quaternion = gxxgeom.base.quaternion(0.71, 0, 0.71, 0)

def vhandler():
	camera.quaternion = gxxgeom.base.quaternion(0.71, 0, 0, 0.71)

def bhandler():
	camera.quaternion = gxxgeom.base.quaternion(0.7, 0.3, -0.55, -0.3)
	camera.quaternion.self_normalize()

gui.addKeyHandler(ord('Z'), zhandler)
gui.addKeyHandler(ord('X'), xhandler)
gui.addKeyHandler(ord('C'), chandler)
gui.addKeyHandler(ord('V'), vhandler)
gui.addKeyHandler(ord('B'), bhandler)

pnts = [
	(0,		0,		0),
	(100,	0,		0),
	(100,	100,	0),
	(0,		100,	0),
	(0,		0,		100),
	(100,	0,		100),
	(100,	100,	100),
	(0,		100,	100),


	(200,  50,	50),
	(50,  300,	50),
	(50,  50,	100),

	(2000, 0,   0),
	(0,   2000, 0),
	(0,   0,   2000),

]

render.add_line(pnts[0], pnts[1])
render.add_line(pnts[1], pnts[2])
render.add_line(pnts[2], pnts[3])
render.add_line(pnts[3], pnts[0])
render.add_line(pnts[4], pnts[5])
render.add_line(pnts[5], pnts[6])
render.add_line(pnts[6], pnts[7])
render.add_line(pnts[7], pnts[4])
render.add_line(pnts[0], pnts[4])
render.add_line(pnts[1], pnts[5])
render.add_line(pnts[2], pnts[6])
render.add_line(pnts[3], pnts[7])

render.add_line(pnts[1], pnts[8])
render.add_line(pnts[2], pnts[8])
render.add_line(pnts[6], pnts[8])
render.add_line(pnts[5], pnts[8])

render.add_line(pnts[3], pnts[9])
render.add_line(pnts[2], pnts[9])
render.add_line(pnts[6], pnts[9])
render.add_line(pnts[7], pnts[9])

#render.add_line(pnts[4], pnts[10])
#render.add_line(pnts[5], pnts[10])
#render.add_line(pnts[6], pnts[10])
#render.add_line(pnts[7], pnts[10])

render.add_line(pnts[0], pnts[11])
render.add_line(pnts[0], pnts[12])
render.add_line(pnts[0], pnts[13])

#render.add_line(pnts[0+4], pnts[1+4])
#render.add_line(pnts[0+4], pnts[2+4])
#render.add_line(pnts[0+4], pnts[3+4])
#render.add_line(pnts[1+4], pnts[2+4])
#render.add_line(pnts[1+4], pnts[3+4])
#render.add_line(pnts[2+4], pnts[3+4])

#monitor.draw_line(points[1], points[2])
#monitor.draw_line(points[2], points[3])
#monitor.draw_line(points[3], points[0])
#
#
#monitor.draw_circle((250,250), 20)
#
#monitor.clear()

gui.exec()