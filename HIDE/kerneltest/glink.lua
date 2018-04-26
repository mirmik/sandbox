local files = find.findInTree("../../genos", ".*.gll$", ".*HIDE.*")
script:evalFile(files, _ENV)

ruller = CXXDeclarativeRuller.new{
	buildutils = { 
		CXX = "g++", 
		CC = "gcc", 
		LD = "ld", 
	},
	weakRecompile = "noscript",
	optimization = "-O2",
	standart = {
		cxx = "-std=gnu++14",
		cc = "-std=gnu11",
	},
	flags = {
		allcc = "-Wl,--gc-sections -fdata-sections -ffunction-sections -pthread",
		cc = "",
		cxx = "",
		ld = "",
	},
	builddir = "./build",
}

Module("main", {
	sources = {
		cxx = "main.cpp",
	},

	includePaths = ".",
	
	modules = {
		{name = "genos.dprint", impl = "diag"},
		{name = "genos.diag", impl = "impl"},
		{name = "genos.arch.linux32"},
		{name = "genos.board.noboard"},

		{name = "genos.atomic_section", impl = "std::mutex"},
		{name = "genos.kernel.scheduler", impl = "standart"},
		{name = "genos.kernel.standart_glue"},
		{name = "genos.kernel.ipcstack"},
		--{name = "genos.kernel.message"},
		{name = "placenew"},
--		{name = "gxx.base"},
--		{name = "gxx.bytearray"},
		{name = "genos.kernel.schedee"},
		{name = "genos.kernel.pool"},
	},

	includeModules = {
		{name = "genos.include"},
		{name = "genos.include.arch.linux32"},
		{name = "genos.include.board.noboard"},
	},
})

local ret = ruller:standartAssemble("main", {
	target = "target",
	targetdir = ".",
	assembletype = "application"
})

if not ret then print(text.yellow("Nothing to do")) end 