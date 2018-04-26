import rabbit.geom2 as g2

class vertex:
	def __init__(self, pnt):
		self.pnt = pnt
		
class edge:
	def __init__(self, crv):
		self.crv = crv

	def connect_next(self, edg):
		connect_edge_edge(self, edg)

	def start(self): return self.crv.start()
	def finish(self): return self.crv.finish()

	def divide(self, t):
		e = edge(g2.curve_segment(self.crv.crv, t, self.crv.bmax))
		self.crv.bmax = t
		enext = self.enext
		self.w.arr.append(e)
		connect_edge_edge(self, e)
		connect_edge_edge(e, enext)

	def __repr__(self):
		return self.crv.__repr__()

def connect_edge_edge(edg1, edg2):
	v = vertex(edg1.finish())
	v.enext = edg2
	v.eprev = edg1
	edg1.vnext = v
	edg2.vprev = v
	edg1.enext = edg2
	edg2.eprev = edg1

class wire:
	def __init__(self, *args): 
		self.arr = []
		self.closed = False 
		for a in args: self.add_edge(a)
		self.try_close()

	def try_close(self):
		if self.arr[0].start().is_same(self.arr[-1].finish()):
			self.closed = True

	def add_edge(self, crv):
		e = edge(crv)
		e.w = self
		self.arr.append(e)
		if len(self.arr) == 1: return
		self.arr[-2].connect_next(e)

	def __repr__(self):
		return self.arr.__repr__()

class figure:
	def __init__(self, *args):
		self.arr = [] 
		for a in args: self.add_wire(a)

	def add_wire(self,a):
		self.arr.append(a)
