import gxxgeom.surface as surface
import gxxgeom.curve as curve
import gxxgeom.util as util
import gxxgeom.base as base
import math

class surface_intersection_logical_error(BaseException):
	def __init__(self, str):
		self.str = str

def surface_intersection_sphere_sphere(sph1, sph2):
	r1 = sph1.rad()
	r2 = sph2.rad()
	d = sph1.loc().distance_to_point(sph2.loc())

	if d == 0:
		if r1 == r2:
			raise surface_intersection_logical_error("equal sphere intersection")
		return []

	if r1 + r2 < d or r1 > d + r2 or r2 > d + r1:
		return []

	koeff = (d**2 + r1**2 - r2**2) / (2 * d)
	koeff /= d

	center = util.linear_interpolation(sph1.loc(), sph2.loc(), koeff)
	cr = - math.sqrt(-(-d + r1 - r2) * (-d + r1 + r2) * (d + r1 - r2) * (d + r2 + r2)) / (2 * d) 
	ax2 = base.axis2(center, norm = base.direction(sph1.loc(), sph2.loc()))
	res = curve.circle(radius = cr, plane = ax2)

	return [res] 



def surface_intersection(surf1, surf2):
	t1 = type(surf1)
	t2 = type(surf2)

	if (t1,t2) in surface_intersection_methods:
		return surface_intersection_methods[(t1,t2)](surf1, surf2)
	elif (t2,t1) in surface_intersection_methods:
		return surface_intersection_methods[(t2,t1)](surf2, surf1)

surface_intersection_methods = {
	(surface.sphere_surface, surface.sphere_surface) : surface_intersection_sphere_sphere,  
}