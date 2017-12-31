import numpy as np
import math
import gxxgeom.base

class Monitor:
	def __init__(self, width, height):
		self.array = np.zeros((width, height))
		self.width = width
		self.height = height

	def clear(self):
		self.array = np.zeros((self.width, self.height))

	def set_pixel(self, x, y):
		if (x < 0 or x >= self.width or y < 0 or y >= self.height): 
			return
		self.array[x,y] = 255

	def draw_line(self, pnt1, pnt2):
		x1 = int(pnt1[0]+0.5); y1 = int(pnt1[1]+0.5); x2 = int(pnt2[0]+0.5); y2 = int(pnt2[1]+0.5)
		dx = x2 - x1
		dy = y2 - y1
		
		sign_x = 1 if dx>0 else -1 if dx<0 else 0
		sign_y = 1 if dy>0 else -1 if dy<0 else 0
		
		if dx < 0: dx = -dx
		if dy < 0: dy = -dy
		
		if dx > dy:
			pdx, pdy = sign_x, 0
			es, el = dy, dx
		else:
			pdx, pdy = 0, sign_y
			es, el = dx, dy
		
		x, y = x1, y1
		
		error, t = el/2, 0        
		
		self.set_pixel(x, y)
		
		while t < el:
			error -= es
			if error < 0:
				error += el
				x += sign_x
				y += sign_y
			else:
				x += pdx
				y += pdy
			t += 1
			self.set_pixel(x, y)

	def draw_circle(self, center, radius):
		x0 = center[0]; y0 = center[1]
		x = 0
		y = radius
	
		delta = 1 - 2 * radius
		error = 0
		
		while y >= 0:
			self.set_pixel(x0 + x, y0 + y)
			self.set_pixel(x0 + x, y0 - y)
			self.set_pixel(x0 - x, y0 + y)
			self.set_pixel(x0 - x, y0 - y)
			error = 2 * (delta + y) - 1
			
			if delta < 0 and error <= 0:
				x+=1
				delta += 2 * x + 1;
				continue
		
			error = 2 * (delta - x) - 1;
			if delta > 0 and error > 0:
				y-=1
				delta += 1 - 2 * y
				continue
			
			x+=1
			delta += 2 * (x - y);
			y-=1;
#	}
#}

class Camera:
	def __init__(self, scene, camera):
		#self.distance = 500
		self.center = np.array([0,0,0])
		self.quaternion = gxxgeom.base.quaternion()
		#self.matrix = np.array([[1,0,0],[0,1,0],[0,0,1]])

		self.yaw = -1
		self.pitch = -1.3
		self.scale = 1

		self.rk = 2
		self.mode = False
		self.evaluate_transformation_matrix()

	def change_mode():
		self.mode = not self.mode	

	def evaluate_transformation_matrix(self):
		if self.mode:
			self.transmat = self.quaternion.rotation_matrix()
		else:
			yawM = np.array([
				[math.cos(self.yaw), -math.sin(self.yaw), 0],
				[math.sin(self.yaw), +math.cos(self.yaw), 0],
				[0				   , 0					, 1],
			])

			pitchM = np.array([
				[math.cos(self.pitch), 	0, 					math.sin(self.pitch)],
				[0, 					1, 					0],
				[-math.sin(self.pitch),	0, 					+math.cos(self.pitch)],
			])

			self.transmat = pitchM.dot(yawM)
			
		scaleM = np.array([
			[self.scale, 0, 0],
			[0, self.scale, 0],
			[0,	0, self.scale],
		])

		self.transmat = scaleM.dot(self.transmat)
			#return yawM

	#def rotation_matrix(self):
	#	if self.mode:
	#		return self.quaternion.rotation_matrix()
	#	else:
	#		yawM = np.array([
	#			[math.cos(self.yaw), -math.sin(self.yaw), 0],
	#			[math.sin(self.yaw), +math.cos(self.yaw), 0],
	#			[0				   , 0					, 1],
	#		])
#
	#		pitchM = np.array([
	#			[math.cos(self.pitch), 	0, 					math.sin(self.pitch)],
	#			[0, 					1, 					0],
	#			[-math.sin(self.pitch),	0, 					+math.cos(self.pitch)],
	#		])
#
	#		return pitchM.dot(yawM)
		
	def transformation_matrix(self):
		return self.transmat

	def xevent(self, i):
		if self.mode:
			self.quaternion = self.quaternion.small_rotate1(i * 0.001)
		else:
			self.yaw -= i * 0.001 * self.rk
		self.evaluate_transformation_matrix()

	def yevent(self, i):
		if self.mode:
			self.quaternion = self.quaternion.small_rotate2(i * 0.001)
		else:
			self.pitch += i * 0.001 * self.rk
		self.evaluate_transformation_matrix()

	def xstrfevent(self, i):
		rotmat = np.linalg.inv(self.transformation_matrix())
		mvec = np.array([0,i,0])
		rvec = rotmat.dot(mvec)
		self.center = np.add(self.center, rvec)
		#self.evaluate_transformation_matrix()
		
	def ystrfevent(self, i):
		rotmat = np.linalg.inv(self.transformation_matrix())
		mvec = np.array([-i,0,0])
		rvec = rotmat.dot(mvec)
		self.center = np.add(self.center, rvec)
		#self.evaluate_transformation_matrix()
		#print(self.center)
		

	def zevent(self, i):
		#if self.mode:
		#	pass
		#else:
		if i > 0:
			self.scale *= 1.1
		else:
			self.scale /= 1.1 
		self.evaluate_transformation_matrix()


	def __repr__(self):
		return self.position.__repr__() + " " + self.quaternion.__repr__()
	#	self.camera = camera
	#	self.scene = scene

	#def render(self):
	#	monitor.clear()
	#	for s in self.scene.shapes:
	#		self.render_shape(s)

	#def render_shape(self, shp):
	#	pass
