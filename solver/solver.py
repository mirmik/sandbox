#!/usr/bin/env python3

import numpy
import scipy
from zencad.libs.screw import screw
import sys

numpy.set_printoptions(threshold=sys.maxsize, linewidth=200, precision=2)

def formal_coefficients_1d_to_2d(self):
	x, y = self.xy_from_vertices()

	a = [0] * 2
	b = [0] * 2
	
	for i in range(4):
		a_ = numpy.linalg.det([
			[x[1],y[1]],
			[x[2],y[2]]
		])

		b_ = -numpy.linalg.det([
			[1,y[1]],
			[1,y[2]]
		])

		c_ = -numpy.linalg.det([
			[x[1],1],
			[x[2],1],
		])			

		x = self.cyclic_shift(x)
		y = self.cyclic_shift(y)

		a[i] = a_ * (-1)**i
		b[i] = b_ * (-1)**i
		c[i] = c_ * (-1)**i

	return a, b, c

def formal_coefficients_3d(self):
	x, y, z = self.xyz_from_vertices()

	a = [0] * 4
	b = [0] * 4
	c = [0] * 4
	d = [0] * 4

	six_V = numpy.linalg.det([
		[1,x[0], y[0], z[0]],
		[1,x[1], y[1], z[1]],
		[1,x[2], y[2], z[2]],
		[1,x[3], y[3], z[3]]
	])

	for i in range(4):
		a_ = numpy.linalg.det([
			[x[1],y[1],z[1]],
			[x[2],y[2],z[2]],
			[x[3],y[3],z[3]]
		])

		b_ = -numpy.linalg.det([
			[1,y[1],z[1]],
			[1,y[2],z[2]],
			[1,y[3],z[3]]
		])

		c_ = -numpy.linalg.det([
			[x[1],1,z[1]],
			[x[2],1,z[2]],
			[x[3],1,z[3]]
		])			

		d_ = -numpy.linalg.det([
			[x[1],y[1],1],
			[x[2],y[2],1],
			[x[3],y[3],1]
		])

		x = self.cyclic_shift(x)
		y = self.cyclic_shift(y)
		z = self.cyclic_shift(z)

		a[i] = a_ * (-1)**i
		b[i] = b_ * (-1)**i
		c[i] = c_ * (-1)**i
		d[i] = d_ * (-1)**i

	return a, b, c, d
	


class FEM:
	def set_solver_indexes_map(self, indexes_map):
		self.solver_element_indexes = indexes_map

	def place_stiffness_matrix(self, matrix):
		dim = self.vertdim()
		blocks = self.stiffness_matrix_as_blocks()
		for i in range(len(self.vertices)):
			mi = self.solver_element_indexes[i]
			for j in range(len(self.vertices)):
				mj = self.solver_element_indexes[j]
				a = dim*mi
				b = dim*mj 
				matrix[a:a+dim,b:b+dim] += blocks[i][j]	

	def stiffness_matrix(self):
		B = self.deformation_matrix()
		Bt = B.transpose()
		D = self.elastic_matrix()
		return numpy.matmul(Bt, numpy.matmul(D,B))

class LinearFEM2(FEM):
	def __init__(self):
		self.Poisson = 0.25 # 0.25 for steel
		self.elastic_modulus = 1		

	def elastic_matrix(self):
		E = self.elastic_modulus
		v = self.Poisson
		return E*(1-v)/(1+v)/(1-2*v) * numpy.array([
			[        1, v/(1-v),               0],
			[  v/(1-v),       1,               0],
			[        0,       0, (1-2*v)/2/(1-v)],
		])

	def xy_from_vertices(self):
		x = [ v[0] for v in self.vertices ]
		y = [ v[1] for v in self.vertices ]
		return x, y

	def vertex_deformation_matrix(self, i):
		return (
				numpy.array([
					[self.b[i],         0],
					[        0, self.c[i]],
					[self.c[i], self.b[i]],
				])
			)

	def baricentric_matrix(self):
		x, y = self.xy_from_vertices()
		return numpy.array([
			[ x[0], x[1], x[2] ],
			[ y[0], y[1], y[2] ],
			[    1,    1,    1 ]
		])

	def pseudo_inverse_baricentric_matrix(self):
		return numpy.linalg.pinv(self.baricentric_matrix())

	def inverse_baricentric_matrix(self):
		if len(self.vertices) == 2:
			x, y = self.xy_from_vertices()
			return numpy.array([
				[y[1]-y[0], x[0]-x[1], x[1]*y[0]-x[0]*y[1]],
				[y[0]-y[1], x[1]-x[0], x[0]*y[1]-x[1]*y[0]],
				[        0,         0,                   0],
			])

		return numpy.linalg.inv(self.baricentric_matrix())

	def formal_coefficients(self):
		x, y = self.xy_from_vertices()

		a = [0] * 3
		b = [0] * 3
		c = [0] * 3
		
		for i in range(3):
			a_ = numpy.linalg.det([
				[x[1],y[1]],
				[x[2],y[2]]
			])

			b_ = -numpy.linalg.det([
				[1,y[1]],
				[1,y[2]]
			])

			c_ = -numpy.linalg.det([
				[x[1],1],
				[x[2],1],
			])			

			x = self.cyclic_shift(x)
			y = self.cyclic_shift(y)

			a[i] = a_ * (-1)**i
			b[i] = b_ * (-1)**i
			c[i] = c_ * (-1)**i

		return a, b, c


class LinearFEM3(FEM):
	def __init__(self):
		self.Poisson = 0.25 # 0.25 for steel
		self.elastic_modulus = 1		

	def elastic_matrix(self):
		E = self.elastic_modulus
		v = self.Poisson
		return E*(1-v)/(1+v)/(1-2*v) * numpy.array([
			[        1, v/(1-v), v/(1-v),               0,               0,               0],
			[  v/(1-v),       1, v/(1-v),               0,               0,               0],
			[  v/(1-v), v/(1-v),       1,               0,               0,               0],
			[        0,       0,       0, (1-2*v)/2/(1-v),               0,               0],
			[        0,       0,       0,               0, (1-2*v)/2/(1-v),               0],
			[        0,       0,       0,               0,               0, (1-2*v)/2/(1-v)]
		])

	def vertex_deformation_matrix(self, i):
		return (1/self.V6*
				numpy.array([
					[self.b[i],         0,         0],
					[        0, self.c[i],         0],
					[        0,         0, self.d[i]],
					[        0, self.d[i], self.c[i]],
					[self.d[i],         0, self.b[i]],
					[self.c[i], self.b[i],         0],
				])
			)

	def xyz_from_vertices(self):
		x = [ v[0] for v in self.vertices ]
		y = [ v[1] for v in self.vertices ]
		z = [ v[2] for v in self.vertices ]
		return x, y, z

class RodFEM2(LinearFEM2):
	def __init__(self, vertices):
		super().__init__()
		self.vertices = [ numpy.array(v) for v in vertices ]

	def stiffness_matrix(self):
		E = self.Poisson
		I = 1 # ???
		l = numpy.linalg.norm(self.vertices[0] - self.vertices[1]) 

		return numpy.array([
			[  12*E*I/l**3,  6*E*I/l**2, -12*E*I/l**3,  6*E*I/l**2],
			[   6*E*I/l**2,  4*E*I/l**1,  -6*E*I/l**2,  2*E*I/l**1],
			[ -12*E*I/l**3, -6*E*I/l**2,  12*E*I/l**3, -6*E*I/l**2],
			[   6*E*I/l**2,  2*E*I/l**1,  -6*E*I/l**2,  4*E*I/l**1],
		])

	def stiffness_matrix_as_blocks(self):
		stiffness = self.stiffness_matrix()
		blocks = [
			[stiffness[ 0:2,0:2], stiffness[ 0:2,2:4]],
			[stiffness[ 2:4,0:2], stiffness[ 2:4,2:4]],
		]
		return blocks

	def vertdim(self):
		return 2


class RodFEM3(LinearFEM3):
	def __init__(self, vertices):
		super().__init__()
		self.density = 1000
		self.vertices = [ numpy.array(v) for v in vertices ]
		self.a, self.b, self.c, self.d = self.formal_coefficients()

class SimplexFEM2(LinearFEM2):
	def __init__(self, vertices):
		super().__init__()
		self.density = 1000
		self.vertices = [ numpy.array(v) for v in vertices ]
		self.reverse_if_need()
		self.a, self.b, self.c = self.formal_coefficients()
		self.S = self.area()
		self.solver_element_indexes = {}

	def vertdim(self):
		return 2

	def area(self):
		x, y = self.xy_from_vertices()
		return numpy.linalg.det([
			[1,x[0], y[0]],
			[1,x[1], y[1]],
			[1,x[2], y[2]],
		])

		
	def reverse_if_need(self):
		area = self.area()
		if (area < 0):
			self.vertices = [ self.vertices[0], self.vertices[2], self.vertices[1] ]

	def cyclic_shift(self, a):
		return a[1:3] + a[0:1]  

	def deformation_matrix(self):
		B0 = self.vertex_deformation_matrix(0)
		B1 = self.vertex_deformation_matrix(1)
		B2 = self.vertex_deformation_matrix(2)
		return numpy.concatenate((B0,B1,B2), axis=1)

	def stiffness_matrix_as_blocks(self):
		stiffness = self.stiffness_matrix()
		blocks = [
			[stiffness[ 0:2,0:2], stiffness[ 0:2,2:4], stiffness[ 0:2,4:6]],
			[stiffness[ 2:4,0:2], stiffness[ 2:4,2:4], stiffness[ 2:4,4:6]],
			[stiffness[ 4:6,0:2], stiffness[ 4:6,2:4], stiffness[ 4:6,4:6]],
		]
		return blocks

class SimplexFEM3(LinearFEM3):
	def __init__(self, vertices):
		super().__init()
		self.density = 1000
		self.Poisson = 0.25 # 0.25 for steel
		self.elastic_modulus = 1
		self._node_deformation = screw()

		self.vertices = vertices
		self.reverse_if_need()
		self.V6, self.a, self.b, self.c, self.d = self.formal_coefficients()
		print(self.V6)

		self.solver_element_indexes = {}

	def vertdim(self):
		return 3

	def reverse_if_need(self):
		x, y, z = self.xyz_from_vertices()
		six_V = numpy.linalg.det([
			[1,x[0], y[0], z[0]],
			[1,x[1], y[1], z[1]],
			[1,x[2], y[2], z[2]],
			[1,x[3], y[3], z[3]]
		])
		if (six_V < 0):
			self.vertices = [
				self.vertices[0], 
				self.vertices[1], 
				self.vertices[3], 
				self.vertices[2]
			]

	def cyclic_shift(self, a):
		#return a[3:] + a[0:3]  
		return a[1:4] + a[0:1]  

	def deformation_matrix(self):
		B0 = self.vertex_deformation_matrix(0)
		B1 = self.vertex_deformation_matrix(1)
		B2 = self.vertex_deformation_matrix(2)
		B3 = self.vertex_deformation_matrix(3)		
		return numpy.concatenate((B0,B1,B2,B3), axis=1)

	def formal_coefficients(self):
		x, y, z = self.xyz_from_vertices()

		a = [0] * 4
		b = [0] * 4
		c = [0] * 4
		d = [0] * 4

		six_V = numpy.linalg.det([
			[1,x[0], y[0], z[0]],
			[1,x[1], y[1], z[1]],
			[1,x[2], y[2], z[2]],
			[1,x[3], y[3], z[3]]
		])

		for i in range(4):
			a_ = numpy.linalg.det([
				[x[1],y[1],z[1]],
				[x[2],y[2],z[2]],
				[x[3],y[3],z[3]]
			])

			b_ = -numpy.linalg.det([
				[1,y[1],z[1]],
				[1,y[2],z[2]],
				[1,y[3],z[3]]
			])

			c_ = -numpy.linalg.det([
				[x[1],1,z[1]],
				[x[2],1,z[2]],
				[x[3],1,z[3]]
			])			

			d_ = -numpy.linalg.det([
				[x[1],y[1],1],
				[x[2],y[2],1],
				[x[3],y[3],1]
			])

			x = self.cyclic_shift(x)
			y = self.cyclic_shift(y)
			z = self.cyclic_shift(z)

			a[i] = a_ * (-1)**i
			b[i] = b_ * (-1)**i
			c[i] = c_ * (-1)**i
			d[i] = d_ * (-1)**i

		return six_V, a, b, c, d

	def stiffness_matrix_as_blocks(self):
		stiffness = self.stiffness_matrix()
		blocks = [
			[stiffness[ 0:3,0:3], stiffness[ 0:3,3:6], stiffness[ 0:3,6:9], stiffness[ 0:3,9:12]],
			[stiffness[ 3:6,0:3], stiffness[ 3:6,3:6], stiffness[ 3:6,6:9], stiffness[ 3:6,9:12]],
			[stiffness[ 6:9,0:3], stiffness[ 6:9,3:6], stiffness[ 6:9,6:9], stiffness[ 6:9,9:12]],
			[stiffness[9:12,0:3], stiffness[9:12,3:6], stiffness[9:12,6:9], stiffness[9:12,9:12]],
		]
		return blocks

	def place_stiffness_matrix(self, matrix):
		blocks = self.stiffness_matrix_as_blocks()
		for i in range(len(self.vertices)):
			mi = self.solver_element_indexes[i]
			for j in range(len(self.vertices)):
				mj = self.solver_element_indexes[j]
				a = 3*mi
				b = 3*mj
				matrix[a:a+3,b:b+3] += blocks[i][j]	

		

class FiniteElementSolver:
	def __init__(self):
		self.elements = []
		self.vertexes_map = {}
		self.index_counter = 0

	def hash_of_vertex(self, v):
		if len(v) == 3:
			return hash(v[0]) + hash(v[1])*52435435 + hash(v[2])*241234 
		elif len(v) == 2:
			return hash(v[0]) + hash(v[1])*52435435 +341234
			

	def get_index_for_vertex(self, vertex):
		vhash = self.hash_of_vertex(vertex)
		if vhash in self.vertexes_map:
			return self.vertexes_map[vhash]
		else:
			self.vertexes_map[vhash] = self.index_counter
			idx = self.index_counter
			self.index_counter += 1
			return idx

	def add(self, elem):
		self.elements.append(elem)
		solver_element_indexes = [self.get_index_for_vertex(v) 
			for i, v in enumerate(elem.vertices)]
		elem.set_solver_indexes_map(solver_element_indexes)

	def vertices_count(self):
		"""Dof of system"""
		return self.index_counter

	def stiffness_matrix(self):
		dim = self.dim()
		matrix = numpy.zeros([dim, dim])
		for elem in self.elements:
			elem.place_stiffness_matrix(matrix)
		return matrix

	def dim(self):
		return self.vertices_count() * self.elements[0].vertdim()

	def vertdim(self):
		return self.elements[0].vertdim()

	def subvec_for_index(self, arr, index):
		vec = numpy.zeros([self.dim()])
		vec[index*self.vertdim():(index+1)*self.vertdim()] = arr
		return vec

def fems_of_square():
	return [
		SimplexFEM2([[0,0],[1,1],[1,0]]), # red
		SimplexFEM2([[0,0],[1,1],[0,1]]), # blue
	]

def fems_of_cube():
	return [
		SimplexFEM3([[0,0,0],[1,1,1],[1,0,1],[0,0,1]]), # red
		SimplexFEM3([[0,0,0],[1,1,1],[1,0,1],[1,0,0]]), # blue
		SimplexFEM3([[0,0,0],[1,1,1],[0,1,1],[0,0,1]]), # green
		SimplexFEM3([[0,0,0],[1,1,1],[0,1,1],[0,1,0]]), # yellow
		SimplexFEM3([[0,0,0],[1,1,1],[1,1,0],[1,0,0]]), # orange
		SimplexFEM3([[0,0,0],[1,1,1],[1,1,0],[0,1,0]]), # violet
	]


if __name__ == "__main__":
	fems = [
		RodFEM2([[0,0], [10,0]])
	]

	print(fems[0].stiffness_matrix())
	#print(fems[0].compliance_matrix())
#	print(numpy.matmul(fems[0].inverse_baricentric_matrix(), numpy.array([[0],[0],[1]])))

	solver = FiniteElementSolver()
	for f in fems:
		solver.add(f)

	stiffness = solver.stiffness_matrix()
	print(stiffness)
	
	index = solver.get_index_for_vertex([0,0])
	deform = solver.subvec_for_index([0,1], index=index)
	
	res = numpy.matmul(stiffness, deform)
	print()
	print(index, res)

