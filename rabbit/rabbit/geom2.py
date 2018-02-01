import math

class vector:
	def __init__(self, x, y): self.x = x; self.y = y
	def abs(self): return math.sqrt(self.x*self.x + self.y*self.y)
	def abs0(self): return max(abs(self.x), abs(self.y))
	def as_unit_vector(self): a = self.abs(); return vector(self.x / a, self.y / a)
	def __sub__(self, oth): return vector(self.x - oth.x, self.y - oth.y)
	def __add__(self, oth): return vector(self.x + oth.x, self.y + oth.y)
	def __repr__(self): return "({},{})".format(self.x, self.y)
	def scale(self, scl): return vector(self.x * scl, self.y * scl)
	def is_same(self, oth): return (self-oth).abs0() < 0.000000001

class curve:
	def __init__(self): print("make curve")

class infline_curve(curve):
	def __init__(self, a, b):
		self.l = a
		self.d = b.as_unit_vector()
		
	def d0(self, t): return self.l + self.d.scale(t)
	def __repr__(self): return "line(l:{},d:{})".format(self.l, self.d)

class circle_curve(curve):
	def __init__(self, r, l, dirx = vector(1,0)):
		self.l = l
		self.r = r
		self.dx = dx
		self.sp = math.atan2(dx.y, dx.x)
	
	def d0(self, t):
		c = cos(t+sp) 
		s = sin(t+sp)
		return vector(l.x + c*r, l.y + s*r)
		
class curve_segment(curve):
	def __init__(self, crv, bmin, bmax):
		self.crv = crv
		self.bmin = bmin
		self.bmax = bmax

	def d0(self, t): return self.crv.d0(t)
	def start(self): return self.crv.d0(self.bmin)
	def finish(self): return self.crv.d0(self.bmax)
	def __repr__(self): return "seg({},n:{},x:{})".format(self.crv, self.bmin, self.bmax)

def line(a, b): s = b - a; return curve_segment(infline_curve(a,s), 0, s.abs())
def circle(r, p): return curve_segment(circle_curve(r,p),0,2*math.pi)