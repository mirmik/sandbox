class vector3:
	def __init__(self, x, y, z):
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
		self.a11 = 1
		self.a12 = 0
		self.a13 = 0
		self.a21 = 0
		self.a22 = 1
		self.a23 = 0
		self.a31 = 0
		self.a32 = 0
		self.a33 = 1
		
class quaternion:
	def __init__(self):
		self arr = np.narray([1,0,0,0])

	def self_normalize(self):
		arr.normalize()

	def __repr__(self):
		return arr.__repr__()

