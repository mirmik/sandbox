class vector2:
	def __init__(self, *args):
		self.arr = [0]*2
		if len(args) == 0:
			pass
		elif len(args) == 1:
			self.arr[0] = args[0][0]
			self.arr[1] = args[0][1]
		else: 
			self.arr[0] = args[0]
			self.arr[1] = args[1]

	def scale(self,scl):
		return vector2(self.x() * scl, self.y() * scl)

	def __add__(self, oth):
		return vector2(self.x() + oth.x(), self.y() + oth.y())

	def __sub__(self, oth):
		return vector2(self.x() - oth.x(), self.y() - oth.y())

	def __repr__(self):
		return "({},{})".format(self.x(), self.y())

	def __getitem__(self, i):
		return self.arr[i]

	def abs(self):
		return np.linalg.norm(self.arr)

	def normalize(self):
		a = self.abs()
		return vector(self.x()/a, self.y()/a)

	def x(self):
		return self.arr[0]

	def y(self):
		return self.arr[1]

class direction2(vector2):
	pass

class point2(vector2):
	pass