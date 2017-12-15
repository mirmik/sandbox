import numpy as np

class Scene:
	def __init__(self):
		self.shapes = []

	def add(shp):
		self.shapes.append(shp)

class Render:
	def __init__(self):
		self.lines3d = []

	def display(self, camera, monitor):
		rotmat = camera.rotation_matrix()
		center = camera.center

		for l in self.lines3d:
			pnt1 = rotmat.dot(np.array([l[0][0]-center[0], l[0][1]-center[1], l[0][2]]-center[2]))
			pnt2 = rotmat.dot(np.array([l[1][0]-center[0], l[1][1]-center[1], l[1][2]]-center[2]))

			w = monitor.width / 2
			h = monitor.height / 2
			monitor.draw_line((pnt1[0] + w, -pnt1[1] + h), (pnt2[0] + w, -pnt2[1] + h))
			
	def add_line(self, pnt1, pnt2):
		self.lines3d.append((pnt1, pnt2))