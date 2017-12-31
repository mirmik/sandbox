import gxxgeom.surface as surface
import gxxgeom.curve as curve
import gxxgeom.base as base

class topo:
	pass

class vertex(topo):
	def __init__(self, pnt):
		self.pnt = pnt
		self.edgs = []

	def set(edg):
		self.edgs.append(edg)

class edge(topo):
	def __init__(self, crv):
		self.crv = crv

	def set_top(tv):
		self.tv = tv

	def set_bot(tv):
		self.bv = bv

	def set_right(rf):
		self.rf = rf

	def set_left(lf):
		self.lf = lf

class face(topo):
	def __init__(self, surf):
		self.surf = surf

class shell(topo):
	def __init__(self):
		pass