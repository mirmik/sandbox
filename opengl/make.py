#!/usr/bin/env python3

import licant

licant.cxx_application("target",
	sources = ["main.cpp"],
	libs = ["GLEW", "glfw", "GL", "X11", "pthread", "Xrandr", "Xi", "SOIL", "freetype"],
	include_paths=["/usr/include/SOIL", ".", "/usr/include/freetype2", "/usr/include/libpng16"]
)

licant.ex("target")