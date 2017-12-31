from gxxgeom.base import *
import gxxgeom.curve as curve

class SurfaceParametrException(BaseException):
	pass

class surface:
	pass
#	def __init__(self):
#		pass

class analitic_surface(surface):
	pass
	#def vu_check(self, u, v):
	#	return self.vs < v or self.ve > v or self.us < u or self.ue > u 

	#def vu_check_critical(self, u, v):
	#	if not (self.vs < v or self.ve > v or self.us < u or self.ue > u):
	#		raise SurfaceParametrException()

class sphere_surface(analitic_surface):
	def __init__(self, center, radius):
		#self.us = 0
		#self.ue = 2 * math.pi
		#self.vs = -math.pi / 2
		#self.ve = math.pi / 2

		self.r = radius
		self.c = point(center)

	def rad(self):
		return self.r

	def loc(self):
		return self.c

	def d0(self, u, v):
		#self.vu_check_critical(u, v)
		us = math.sin(u)
		vs = math.sin(v)
		uc = math.cos(u)
		vc = math.cos(v)
		return point(
			self.r * vc * uc + self.c.x(),
			self.r * vc * us + self.c.y(),
			self.r * vs + self.c.z(),
		)

	def inv_d0(self, pnt):
		vec = pnt - self.c
		vs = vec.z() / self.r
		v = math.asin(vs)
		vc = math.cos(v)
		uc = vec.x / self.r / vc
		us = vec.y / self.r / vc
		u = math.atan2(uc, us)

	def vcurve(self, v):
		return curve.elipse(self.c, vector(self.r*math.cos(v), self.r*math.sin(v), 0), vector(0, 0, self.r))

	def ucurve(self, u):
		return curve.elipse(self.c + vector(0,0,self.r).scale(math.sin(u)), vector(0,self.r*math.cos(u),0), vector(self.r*math.cos(u),0,0))

	def dispcurves(self):
		ctotal = 5
		circles = [self.vcurve(v) for v in [math.pi / ctotal * t for t in range(0, ctotal)]]
		return circles + [self.ucurve(0), 
			self.ucurve(math.pi/4), 
			self.ucurve(-math.pi/4), 
			self.ucurve(math.pi/8*3), 
			self.ucurve(-math.pi/8*3), 
			self.ucurve(math.pi/8), 
			self.ucurve(-math.pi/8),
		]


class movement_surface(surface):
	pass

class extrude_surface(movement_surface):
	def __init__(self, prof, vec):
		#self.us = prof.tmin
		#self.ue = prof.tmax
		#self.vs = 0
		#self.ve = vec.abs()

		self.prof = prof
		self.vec = vector(vec).normalize()

	def d0(self, u, v):
		return point(self.prof.d0(u) + self.vec.scale(v))
