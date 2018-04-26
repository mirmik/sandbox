#!/usr/bin/env python3

from licant.cxx_modules import application, doit

application("target",
	sources = ["main.cpp"],
	include_paths = ['/usr/include/oce'],
	libs = [
		'TKG2d', 'TKG3d', 'TKBRep', 'TKPrim', 'TKMath', 'TKernel', 'TKGeomBase',
		'TKTopAlgo', 'TKOffset', 'TKBO', 'TKFillet'
	]
)

doit("target")