#!/usr/bin/env python3

import numpy
import scipy

class SimplexFEM:
	def __init__(self):
		self.density = 1000
		self.matrix_mass = []

		self.vertices = [
			[0,0,0],
			[0.1, 0.2, 0.3],
			[0.2, 0.5, 0.4]
		]

		self.solver_indexes_map = {}

	def mass_matrix():
		pass

	def stiffness_matrix():
		pass


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
