#!/usr/bin/env python3

import numpy
import scipy

class SimplexFEM:
	def __init__(self):
		self.density = 1000
		self.Poisson = 0.25 # 0.25 for steel
		self._node_deformation = screw()

		self.vertices = [
			[0,0,0],
			[0.1, 0.2, 0.3],
			[0.2, 0.5, 0.4]
		]

		self.solver_indexes_map = {}

	#def mass_matrix():	

	def formal_coefficients(self, x, y, z):
		a = [0] * 4
		b = [0] * 4
		c = [0] * 4
		d = [0] * 4
		for i in range(4):
			a_ = numpy.array([
				[x[1],y[1],z[1]],
				[x[2],y[2],z[2]],
				[x[3],y[3],z[3]]
			])



			x = cyclic_shift(x)
			y = cyclic_shift(y)
			z = cyclic_shift(z)

			a[i] = a_


	def six_V_coefficient(self):
		x = self.x_vector([0,1,2,3])
		y = self.y_vector([0,1,2,3])
		z = self.z_vector([0,1,2,3])
		six_V = numpy.determinant([
			[1,x[0], y[0], z[0]],
			[1,x[1], y[1], z[1]],
			[1,x[2], y[2], z[2]],
			[1,x[3], y[3], z[3]]
		])


	def stiffness_matrix():
		return []

	def node_movement(self):
		return self._node_movement

	def nondeformed_point_movement(self, vec):
		baricentric_coords = simplex_baricentric(vec, self.vertices)
		return baricentric_coords.dot(self._node_movement)

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
		
