#!/usr/bin/env python3
#coding:utf-8

import os
import licant
import licant.cxx_make

licant.include("nos")
licant.include("igris")
licant.include("crow")
licant.include("ralgo")
licant.include("genos")

avr_binutils = licant.cxx_make.make_gcc_binutils("avr")

licant.cxx_application("firmware.bin",
	binutils = avr_binutils,
	sources = ["main.cpp"], 

	mdepends = [
		"genos.include",
		"genos.irqtbl",
		"genos.systime",
		("genos.board", "arduino_mega"),

		"igris.include",
		
		"igris.libc",
		"igris.posix",
		"igris.std",

		"igris.cxx_support",
		("igris.syslock", "genos.atomic"),
		("igris.dprint", "diag"),
		
		"genos.drivers.avr",

		"nos",
		("nos.current_ostream", "nullptr"),

		"ralgo",
	],

	cxx_flags = "-O3",

)

@licant.routine(deps=["firmware.bin"])
def install():
	os.system("./install.sh")

licant.ex("firmware.bin")