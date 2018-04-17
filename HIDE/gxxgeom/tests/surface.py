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
	updateData()

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

#el = elipse(point(0,0,0), vector(0,100,0), vector(100,0,0))
#el2 = elipse(point(0,0,-100), vector(0,100,0), vector(100,0,0))
#el3 = elipse(point(0,0,-200), vector(0,100,0), vector(100,0,0))
#
#scene.add_curve(el)
#scene.add_curve(el2)
#scene.add_curve(el3)

sph0 = surface.sphere_surface(origin(), 100);
sph1 = surface.sphere_surface(point(40,0,0), 100);
sph3 = surface.sphere_surface(point(0,300,200), 100);
sph2 = surface.sphere_surface(point(0,500,300), 100);

res = surface_intersection(sph0, sph1)

for i in res:
	scene.add_curve(i)

scene.add_surface(sph0)
scene.add_surface(sph1)
#scene.add_surface(sph2)
#scene.add_surface(sph3)

#scene.ortes = False

updateData()
gui.exec()


#profile = curve.polyline([
#		point(0,0,0),
#		point(1,0,0),
#		point(1,1,0),
#		point(0,1,0)
#	], closed = True
#)

#extrude = surface.extrude_surface(profile, vector(0,0,1))

#print(extrude.d0(0,1))
#print(extrude.d0(1,1))
#print(extrude.d0(2,1))