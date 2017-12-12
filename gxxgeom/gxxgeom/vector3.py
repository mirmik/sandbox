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