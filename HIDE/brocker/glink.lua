script:evalFile("gxx/gxx.gll", _ENV);

ruller = CXXDeclarativeRuller.new{
		buildutils = { 
		CXX = "g++", 
		CC = "gcc", 
		LD = "ld",  
	},
	--weakRecompile = "noscript",
	optimization = "-O2",
	standart = {
		cxx = "-std=gnu++14",
		cc = "-std=gnu11",
	},
	flags = {
		cc = "",
		cxx = "",
		ld = "",
		allcc = "-Wl,--gc-sections -fdata-sections -ffunction-sections"
	},
	builddir = "./build",
}

Module("main", {
	sources = {
		directory = "src",
		cxx = "main.cpp"
	},
})

local ret = ruller:standartAssemble("main", {
	target = "target",
	targetdir = "./",
	assembletype = "application"
})

if not ret then print(text.yellow("Nothing to do")) end