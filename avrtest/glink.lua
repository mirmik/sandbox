print(text.green("Script Start"))

local files = find.findInTree("../../genos", ".*.gll$", ".*HIDE.*")
script:evalFile(files, _ENV)

ruller = CXXDeclarativeRuller.new{
	buildutils = { 
		CXX = "avr-g++", 
		CC = "avr-gcc", 
		LD = "avr-ld", 
	},
	weakRecompile = "noscript",
	optimization = "-Os",
	
	standart = {
		cxx = "-std=gnu++14",
		cc = "-std=gnu11",
	},
	
	flags = {
		cc = "",
		cxx = "-fno-rtti -fexceptions",
		ld = "-nostdinc -nostartfiles",
		allcc = "-nostdlib -lgcc -lm -mmcu=atmega2560 -DF_CPU=16000000 -Wl,--gc-sections -fdata-sections -ffunction-sections"
	},
	
	builddir = "./build"
}

Module("main", {
	sources = {
		cxx = "main.cpp",
	},

	includePaths = ".",
	
	modules = {
		{name = "cxx"},

		{name = "genos.dprint", impl = "diag"},
		{name = "genos.diag", impl = "impl"},
		
		{name = "genos.irqtbl"},
		
		{name = "genos.arch.atmega2560"},
		{name = "genos.board.arduino_mega"},

		--{name = "genos.fs.chardev", impl = "cxx"},
		{name = "genos.arch.atmega2560.drivers.usart", impl = "cxx"},

		{name = "genos.libc"},

		{name = "placenew"},
		{name = "newdel"},
		{name = "genos.lin_malloc"},
		{name = "genos.kernel.ipcstack"},

		{name = "genos.kernel.scheduler", impl = "standart"},
		{name = "genos.atomic_section", impl = "disable_irqs"},
		{name = "genos.kernel.standart_glue"},
		{name = "genos.kernel.schedee"},

		{name = "genos.kernel.utility"},
		{name = "genos.kernel.stdstream"},
	},

	includeModules = {
		{name = "genos.include"},
		{name = "genos.include.libc",},
		{name = "genos.include.arch.atmega2560"},
		{name = "genos.include.board.arduino_mega"},
	},
})

local ret = ruller:standartAssemble("main", {
	target = "target",
	targetdir = "./build",
	assembletype = "application"
})

if not (ret) then print(text.yellow("Nothing to do")) end