#!/usr/bin/env python3

import licant

licant.cxx_application("target",
	sources = ["main.cpp"],
	libs = ["GLEW", "glfw", "GL", "X11", "pthread", "Xrandr", "Xi", "SOIL"],
	include_paths=["/usr/include/SOIL"]
)

licant.ex("target")