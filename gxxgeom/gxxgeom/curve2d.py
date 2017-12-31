import gxxgeom.base2d as base2d

class curve2:
	pass

class circle2(curve2):
	def __init__(self, center, radius):
		self.c = base2d.point2(center)
		self.r = radius

	def rad():
		return self.r

	def loc():
		return self.c

	def d0(self, t):
		return self.c + base2d.vector2(self.r * math.sin(t), self.r * math.cos(t))

class line2(curve2):
	def __init__(self, pnt, vec):
		self.pnt = base2d.point2(pnt)
		self.dir = base2d.direction2(vec)

	def d0(self, t):
		return self.pnt + self.dir.scale(t)