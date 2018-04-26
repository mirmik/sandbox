import numpy as np

class curve_draw_helper:
	def __init__(self, crv):
		self.plg = crv.polygons()
	
	def polygons(self):
		return self.plg

class surface_draw_helper:
	def __init__(self, crv):
		self.plg = crv.dispcurves()
	
	def dispcurves(self):
		return self.plg

class Scene:
	def __init__(self):
		self.shapes = []
		self.surfaces = []
		self.curves = []
		self.ortes = True

	#def add(shp):
	#	self.shapes.append(shp)

	def add_surface(self, surf):
		self.surfaces.append(surface_draw_helper(surf))

	def add_curve(self, crv):
		self.curves.append(curve_draw_helper(crv))

class Render:
	def __init__(self):
		self.lines3d = []

	def display(self, camera, monitor):
		rotmat = camera.transformation_matrix()
		center = camera.center

		#print(len(self.lines3d));
		for l in self.lines3d:
			pnt1 = rotmat.dot(np.array([l[0][0]-center[0], l[0][1]-center[1], l[0][2]-center[2]]))
			pnt2 = rotmat.dot(np.array([l[1][0]-center[0], l[1][1]-center[1], l[1][2]-center[2]]))

			w = monitor.width / 2
			h = monitor.height / 2
			monitor.draw_line((pnt1[0] + w, -pnt1[1] + h), (pnt2[0] + w, -pnt2[1] + h))
			
	def add_line(self, pnt1, pnt2):
		self.lines3d.append((pnt1, pnt2))

	def display_scene(self, scene, camera, monitor):
		self.lines3d.clear()
		
		for surf in scene.surfaces:
			self.draw_surface(surf)

		for crv in scene.curves:
			self.draw_curve(crv)

		if scene.ortes:
			self.draw_ortes()
		
		self.display(camera, monitor)
		

	def draw_curve(self, crv):
		polygons = crv.polygons()
		for p in polygons:
			self.add_line(p.pnt1, p.pnt2)

	def draw_surface(self, surf):
		curves = surf.dispcurves()
		for c in curves:
			polygons = c.polygons()
			for p in polygons:
				self.add_line(p.pnt1, p.pnt2)

	def draw_ortes(self):
		self.add_line((0,0,0), (2000,0,0))
		self.add_line((0,0,0), (0,2000,0))
		self.add_line((0,0,0), (0,0,2000))
