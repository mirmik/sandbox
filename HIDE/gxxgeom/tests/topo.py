#!/usr/bin/env python3
#coding: utf-8

import sys
import math
sys.path.append("..")

from gxxgeom.base import * 
import gxxgeom.surface as surface
from gxxgeom.curve import *
from gxxgeom.gui import *
from gxxgeom.monitor import *
from gxxgeom.render import *
from gxxgeom.surface_ops import *

monitor = Monitor(1000, 1000)
scene = Scene()
camera = Camera(scene, monitor)
render = Render()

def updateData():
	monitor.clear()
	render.display_scene(scene, camera, monitor)
	gui.setData(monitor.array)

def mouseEvent(diff):
	global q
	if diff.x() != 0:
		camera.xevent(diff.x())
	
	if diff.y() != 0:
		camera.yevent(diff.y())
	updateData()


def wheelEvent(angle):
	camera.zevent(angle)
	updateData()

def centerEvent(diff):
	if diff.x() != 0:
		camera.xstrfevent(diff.x())
	
	if diff.y() != 0:
		camera.ystrfevent(diff.y())
	updateData()

	
gui = GUI()
#gui.setTimeoutHandler(updateData)
gui.connectMouseHandler(mouseEvent)
gui.connectWheelHandler(wheelEvent)
gui.connectCenterHandler(centerEvent)

def zhandler():
	#camera.quaternion = gxxgeom.base.quaternion(1, 0, 0, 0)
	camera.yaw = -1
	camera.pitch = -1.3
	camera.scale = 1
	camera.evaluate_transformation_matrix()
	updateData()

def xhandler():
	camera.mode = True
	camera.evaluate_transformation_matrix()
	updateData()

def chandler():
	camera.mode = False
	camera.evaluate_transformation_matrix()
	updateData()

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






updateData()
gui.exec()