#!/usr/bin/env python3

import numpy
import scipy
from zencad.libs.screw import screw

class SimplexFEM:
	def __init__(self, vertices):
		self.density = 1000
		self.Poisson = 0.25 # 0.25 for steel
		self.elastic_modulus = 1
		self._node_deformation = screw()

		self.vertices = vertices

		self.V6, self.a, self.b, self.c, self.d = self.formal_coefficients()

		self.solver_indexes_map = {}

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

	def eval_deformation_matrix(self):
		B0 = self.vertex_deformation_matrix(0)
		B1 = self.vertex_deformation_matrix(1)
		B2 = self.vertex_deformation_matrix(2)
		B3 = self.vertex_deformation_matrix(3)		
		return numpy.concatenate((B0,B1,B2,B3), axis=1)

	def eval_elastic_matrix(self):
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

	def eval_stiffness_matrix(self):
		return 

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

class FlexibleBody:
	def __init__(self):
		self.elements = []

		

class FiniteElementSolver:
	def __init__(self):
		self.elements = []

	def hash_for_vertex(self, vertex):
		pass

	def get_index_for_vertex(self, vertex):
		pass

	def add_element(self, elem):
		self.elements.append(elem)
		solver_element_indexes = [self.get_index_for_vertex(v) 
			for i, v in enumerate(elem.vertices)]
		elem.set_solver_indexes_map(solver_element_indexes)

	def global_mass_matrix(self):
		pass

def fems_of_cube():
	return [
		SimplexFEM([[0,0,0],[1,1,1],[1,0,0],[1,0,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[1,0,0],[0,1,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,1,0],[0,1,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,1,0],[1,1,0]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,0,1],[1,0,1]]),
		SimplexFEM([[0,0,0],[1,1,1],[0,0,1],[0,1,1]]),
	]
		
if __name__ == "__main__":
	fems = fems_of_cube()
	