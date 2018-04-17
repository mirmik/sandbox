import math
import gxxgeom.util as util
from gxxgeom.polygons import line_polygon
from gxxgeom.base import point

class curve:
	pass

class line(curve):
	def __init__(self, pnt1, pnt2):
		self.pnt = pnt1
		self.vec = pnt2 - pnt1

	def d0(self, param):
		return self.pnt + self.vec.scale(param) 

	def polygons(self):
		return [line_polygon(pnt1, pnt2)]

	#def transform(self, trans):
	#	self.pnt = trans(self.pnt)
	#	self.vec = trans(self.vec)

#class polyline(curve):
#	def __init__(self, points, closed = False):
#		self.points = points
#		self.tmax = len(points) - 1
#		self.tmin = 0
#		if closed:
#			self.points.append(self.points[0])
#			self.tmax += 1 
#
#	def d0(self, t):
#		num = int(t)
#		ret = point(util.linear_interpolation(self.points[num], self.points[num + 1], t - num))
#		return ret

class circle(curve):
	def __init__(self, radius, plane):
		self.center = plane.loc()
		self.vecx = plane.dirx().scale(radius)
		self.vecy = plane.diry().scale(radius)

	def d0(self, t):
		return self.center + self.vecx.scale(math.cos(t)) + self.vecy.scale(math.sin(t))

	def polygons(self):
		total = 20
		rng = [ 2 * math.pi / total * t for t in range(0, total + 1) ]
		points = [self.d0(t) for t in rng]
		polygons = [line_polygon(points[i], points[i+1]) for i in range(0,total)]
		polygons.append(line_polygon(points[-1], points[0]))
		return polygons

	def loc(self):
		return self.center

	def dirx(self):
		return self.vecx.normalize()
	
	def diry(self):
		return self.vecy.normalize()
	

class elipse(curve):
	def __init__(self, center, vecx, vecy):
		self.center = center
		self.vecx = vecx
		self.vecy = vecy

	def d0(self, t):
		return self.center + self.vecx.scale(math.cos(t)) + self.vecy.scale(math.sin(t))

	def polygons(self):
		total = 20
		rng = [ 2 * math.pi / total * t for t in range(0, total + 1) ]
		points = [self.d0(t) for t in rng]
		polygons = [line_polygon(points[i], points[i+1]) for i in range(0,total)]
		polygons.append(line_polygon(points[-1], points[0]))
		return polygons


#	def transform(self, trans):
#		self.center = trans(self.center)
#		self.vecx = trans(self.vecx)
#		self.vecy = trans(self.vecy)
#
#class helix(curve):
#	def __init__(self, center, vecx, vec, vecz, maxparam):
#		curve.__init__(self, 0, maxparam)
#		self.center = center
#		self.maxparam = maxparam
#		self.vecx = vecx
#		self.vecy = vecy		
#		self.vecz = vecz		
#
#	def equation(self, t):
#		return (
#			self.center 
#			+ self.vecx.scale(math.cos(t)) 
#			+ self.vecy.scale(math.sin(t)) 
#			+ self.vecz.scale(t)
#		)
#
#	def transform(self, trans):
#		self.center = trans(self.center)
#		self.vecx = trans(self.vecx)
#		self.vecy = trans(self.vecy)
#		self.vecz = trans(self.vecz)
