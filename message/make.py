#!/usr/bin/env python3

from licant.cxx_modules import application, doit
from licant.modules import submodule
from licant.libs import include

include("gxx")

application("target",
	sources = ["main.c"],
	include_paths = ["."],

	include_modules = [
		submodule("gxx"),
		submodule("gxx.print", "cout"),
		submodule("gxx.dprint", "cout"),
	]
)

doit("target")