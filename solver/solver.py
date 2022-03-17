#!/usr/bin/env python3

import numpy
import scipy
from zencad.libs.screw import screw
import sys

numpy.set_printoptions(threshold=sys.maxsize, linewidth=200)

class SimplexFEM:
	def __init__(self, vertices):
		self.density = 1000
		self.Poisson = 0.25 # 0.25 for steel
		self.elastic_modulus = 1
		self._node_deformation = screw()

		self.vertices = vertices

		self.V6, self.a, self.b, self.c, self.d = self.formal_coefficients()

		self.solver_element_indexes = {}

	#def mass_matrix():	

	def xyz_from_vertices(self):
		x = [ v[0] for v in self.vertices ]
		y = [ v[1] for v in self.vertices ]
		z = [ v[2] for v in self.vertices ]
		return x, y, z

	def cyclic_shift(self, a):
		#return a[3:] + a[0:3]  
		return a[1:4] + a[0:1]  

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

	def deformation_matrix(self):
		return self._deformation_matrix

	def deformation_matrix(self):
		B0 = self.vertex_deformation_matrix(0)
		B1 = self.vertex_deformation_matrix(1)
		B2 = self.vertex_deformation_matrix(2)
		B3 = self.vertex_deformation_matrix(3)		
		return numpy.concatenate((B0,B1,B2,B3), axis=1)

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

	def stiffness_matrix(self):
		B = self.deformation_matrix()
		Bt = B.transpose()
		D = self.elastic_matrix()

		return numpy.matmul(Bt, numpy.matmul(D,B))

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

	def set_solver_indexes_map(self, indexes_map):
		self.solver_element_indexes = indexes_map

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

class FlexibleBody:
	def __init__(self):
		self.elements = []

		

class FiniteElementSolver:
	def __init__(self):
		self.elements = []
		self.vertexes_map = {}
		self.index_counter = 0

	def hash_of_vertex(self, v):
		return hash(v[0]) + hash(v[1])*52435435 + hash(v[2])*241234 

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
		return self.vertices_count() * 3

	def subvec_for_index(self, arr, index):
		vec = numpy.zeros([self.dim()])
		vec[index*3:(index+1)*3] = arr
		return vec

def fems_of_cube():
	return [
		SimplexFEM([[0,0,0],[1,1,1],[1,0,0],[1,0,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[1,0,0],[1,1,0]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,1,0],[0,1,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,1,0],[1,1,0]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,0,1],[1,0,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,0,1],[0,1,1]]),
	]
		
if __name__ == "__main__":
	fems = fems_of_cube()
	

	solver = FiniteElementSolver()
	for f in fems:
		solver.add(f)

	#print(fems[1].stiffness_matrix())

	#print(solver.vertices_count())
	#for f in fems:
	#	print(f.solver_element_indexes)

	#print(solver.dim())
	stiffness = solver.stiffness_matrix()

	force = solver.subvec_for_index([0,0,1], index=solver.get_index_for_vertex([1,1,1]))
	res = numpy.matmul(stiffness, force)
	print(res)

	force = solver.subvec_for_index([0,0,1], index=solver.get_index_for_vertex([0,1,1]))
	res = numpy.matmul(stiffness, force)
	print(res)

	force = solver.subvec_for_index([0,0,1], index=solver.get_index_for_vertex([1,0,1]))
	res = numpy.matmul(stiffness, force)
	print(res)

	force = solver.subvec_for_index([0,0,1], index=solver.get_index_for_vertex([0,0,1]))
	res = numpy.matmul(stiffness, force)
	print(res)