import numpy as np
import math

class vector3:
	def __init__(self, x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def scale(self,scl):
		return vector3(self.x * scl, self.y * scl, self.z * scl)

	def __add__(self, oth):
		return vector3(self.x + oth.x, self.y + oth.y, self.z + oth.z)

	def __repr__(self):
		return "({},{},{})".format(self.x, self.y, self.z)

class point(vector3):
	pass

class direction(vector3):
	pass

class vector(vector3):
	pass

class matrix3: 
	def __init__(self):
		pass























class quaternion:
	def __init__(self, q0=1, q1=0, q2=0, q3=0):
		#self.arr = np.array([q0,q1,q2,q3])
		self.q0, self.q1, self.q2, self.q3 = q0, q1, q2, q3

	def abs(self):
		return math.sqrt(self.q0**2+self.q1**2+self.q2**2+self.q3**2)

	def self_normalize(self):
		mod = self.abs()
		self.q0 = self.q0 / mod
		self.q1 = self.q1 / mod
		self.q2 = self.q2 / mod
		self.q3 = self.q3 / mod

	#def normalize(self):
	#	return quaternion(*(self.arr / np.linalg.norm(self.arr)))

	def self_snormalize(self):
		self.q0 = math.sqrt(1 - self.q1 ** 2 + self.q2 ** 2 + self.q3 ** 2)

	def __repr__(self):
		return (self.q0,self.q1,self.q2,self.q3).__repr__()

	def mul(self, other):
		return quaternion(
			+self.q0*other.q0 -self.q1*other.q1 -self.q2*other.q2 -self.q3*other.q3,
			+self.q0*other.q1 +self.q1*other.q0 +self.q2*other.q3 -self.q3*other.q2,
			+self.q0*other.q2 -self.q1*other.q3 +self.q2*other.q0 +self.q3*other.q1,
			+self.q0*other.q3 +self.q1*other.q2 -self.q2*other.q1 +self.q3*other.q0			
		)

	#def rotate_vector(self, x,y,z):
	#	q01 = self.q0*self.q1
	#	q02 = self.q0*self.q2
	#	q03 = self.q0*self.q3
	#	
	#	q11 = self.q1*self.q1
	#	q22 = self.q2*self.q2
	#	q33 = self.q3*self.q3
	#	
	#	q12 = self.q1*self.q2
	#	q13 = self.q1*self.q3
	#	q23 = self.q2*self.q3
	#	
	#	return (
	#		x * (1-2*q22-2*q33) 	+ y * 2*(q12+q03) 			+ z * 2*(q13+q02),
	#		x * 2*(q12+q03)			+ y * (1 - 2*q11 - 2*q33) 	+ z * 2*(q23+q01),
	#		x * 2*(q13+q02)	 		+ y * 2*(q23+q01) 			+ z * (1 - 2*q11- 2*q22),
	#	)

	def rotation_matrix(self):
		qww = self.q0 * self.q0
		qxx = self.q1 * self.q1
		qyy = self.q2 * self.q2
		qzz = self.q3 * self.q3

		qxw = self.q1 * self.q0
		qyw = self.q2 * self.q0
		qzw = self.q3 * self.q0

		qxy = self.q1 * self.q2
		qxz = self.q1 * self.q3

		qyz = self.q2 * self.q3


		mat = np.array([
			[1 - 2*qyy - 2*qzz,		2*qxy - 2*qzw,			2*qxz + 2*qyw],
			[2*qxy + 2*qzw,			1 - 2*qxx - 2*qzz,		2*qyz - 2*qxw],
			[2*qxz - 2*qyw,			2*qyz + 2*qxw,			1 - 2*qxx - 2*qyy]
		])
		return mat

	#res.q0 = a.q0 * b.q0 - a.q1 * b.q1 - a.q2 * b.q2 - a.q3 * b.q3
	#res.q1 = a.q0 * b.q1 + a.q1 * b.q0 + a.q2 * b.q3 - a.q3 * b.q2
	#res.q2 = a.q0 * b.q2 - a.q1 * b.q3 + a.q2 * b.q0 + a.q3 * b.q1
	#res.q3 = a.q0 * b.q3 + a.q1 * b.q2 - a.q2 * b.q1 + a.q3 * b.q0

	def small_rotate1(self, angle):
		#mod = 1/math.sqrt(1 + angle*angle)
		angle /= 2
		nq = quaternion(
			self.q0 - self.q1 * angle,
			self.q1 + self.q0 * angle,
			self.q2 - self.q3 * angle,
			self.q3 + self.q2 * angle
		)
		nq.self_normalize()
		return nq

	def small_rotate2(self, angle):
		angle /= 2
		nq = quaternion(
			self.q0 - self.q2 * angle,
			self.q1 + self.q3 * angle,
			self.q2 + self.q0 * angle,
			self.q3 - self.q1 * angle
		)
		nq.self_normalize()
		return nq


	def small_rotate3(self, angle):
		#mod = 1/math.sqrt(1 + angle*angle)
		angle /= 2
		nq = quaternion(
			self.q0 - self.q3 * angle,
			self.q1 - self.q2 * angle,
			self.q2 + self.q1 * angle,
			self.q3 + self.q0 * angle
		)
		nq.self_normalize()
		return nq
	

	def euler(self):
		return (
			math.atan2(2*(self.q0*self.q1 + self.q2*self.q3), 1-2*(self.q1**2 + self.q2**2)),
			math.asin(2*(self.q0*self.q2-self.q3*self.q1)),
			math.atan2(2*(self.q0*self.q3 + self.q1*self.q2), 1-2*(self.q2**2 + self.q3**2)),
		)