import math

class parametric_curve:
	def __init__(self, start, stop):
		self.start = start
		self.stop = stop

	def point(self, proc):
		inv = 1 - proc
		return self.equation(self.start * inv + self.stop * proc)


class segment(parametric_curve):
	def __init__(self, pnt, vec):
		parametric_curve.__init__(self, 0, 1)
		self.pnt = pnt
		self.vec = vec

	def equation(self, param):
		return self.pnt + self.vec.scale(param) 

	def transform(self, trans):
		self.pnt = trans(self.pnt)
		self.vec = trans(self.vec)

class elips(parametric_curve):
	def __init__(self, center, vecx, vecy):
		parametric_curve.__init__(self, 0, 2*math.pi)
		self.center = center
		self.vecx = vecx
		self.vecy = vecy

	def equation(self, t):
		return self.center + self.vecx.scale(math.cos(t)) + self.vecy.scale(math.sin(t))

	def transform(self, trans):
		self.center = trans(self.center)
		self.vecx = trans(self.vecx)
		self.vecy = trans(self.vecy)

class helix(parametric_curve):
	def __init__(self, center, vecx, vec, vecz, maxparam):
		parametric_curve.__init__(self, 0, maxparam)
		self.center = center
		self.maxparam = maxparam
		self.vecx = vecx
		self.vecy = vecy		
		self.vecz = vecz		

	def equation(self, t):
		return (
			self.center 
			+ self.vecx.scale(math.cos(t)) 
			+ self.vecy.scale(math.sin(t)) 
			+ self.vecz.scale(t)
		)

	def transform(self, trans):
		self.center = trans(self.center)
		self.vecx = trans(self.vecx)
		self.vecy = trans(self.vecy)
		self.vecz = trans(self.vecz)