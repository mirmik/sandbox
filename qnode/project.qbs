import qbs.base 1.0 

Product {
	name: "qnode"
	targetName: "target"
	type: "application"
	Depends { name: "cpp" }
	Depends { name: "Qt"; submodules: ["core", "gui", "opengl"] }
	files: [ 
		"main.cpp", "ColorSlider.h", "CentralFrame.h"
	]

	cpp.includePaths: [ '.' ]
	cpp.cxxLanguageVersion: "c++14"

}