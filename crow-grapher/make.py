#!/usr/bin/env python3

import licant
import os

licant.include("igris")
licant.include("nos")
licant.include("crow")

#os.environ["LD_LIBRARY_PATH"] = "/usr/lib/x86_64-linux-gnu/"

licant.cxx_application("crow-chart",
	mdepends = [
		"crow",
		"igris",

		"crow.udpgate",
		("igris.ctrobj", "linux")
	],

	sources = ["main.cpp"],
	include_paths = [".", 
	"src",
	"/usr/include/x86_64-linux-gnu/qt5/", 
	"/usr/include/x86_64-linux-gnu/qt5/QtCore",
	"/usr/include/x86_64-linux-gnu/qt5/QtWidgets"],

	cxx_flags = "-fPIC",

	moc=["src/DisplayWidget.h"],

	libs=["Qt5Core", "Qt5Gui", "Qt5Widgets"]
)

licant.ex("crow-chart")