import qbs.base 1.0 

Product {
	name: "gcort"
	targetName: "target"
	type: "application"
	Depends { name: "cpp" }
	Depends { name: "Qt"; submodules: ["core", "gui", "opengl" ] }
	
	Group {
        name: "FreeBSD files"
        condition: true
        files: [ "main.cpp", "ImageBoard.h", "FirstCore.h" ]
        prefix: "src/"
    }

	cpp.includePaths: [ '.', 'src' ]
	cpp.cxxLanguageVersion: "c++14"

}