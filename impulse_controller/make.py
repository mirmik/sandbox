#!/usr/bin/env python3
#coding:utf-8

import os
import licant
import licant.cxx_make

licant.include("nos")
licant.include("gxx")
licant.include("crow")
licant.include("ralgo")
licant.include("genos")

avr_binutils = licant.cxx_make.make_gcc_binutils("avr")

licant.cxx_application("firmware.bin",
	binutils = avr_binutils,
	sources = ["main.cpp"], 

	mdepends = [

		"gxx.std",
		"gxx.libc",
		"gxx.posix",
		"gxx.include",
		
		"genos.include",

		("genos.board", "arduino_mega"),
		"genos.irqtbl",
		"genos.systime",
		#"genos.sched",
		"genos.drivers.avr",
		"genos.drivers.gpio.avr",

		("gxx.dprint", "diag"),
		("gxx.syslock", "genos.atomic"),
		"genos.cpudelay",
		"gxx.cxx_support",
		"gxx.panic",
		("genos.malloc", "lin"),
		#"genos.mvfs",
		#("genos.mvfs.schedee_support"),

		"ralgo",
	]

)

@licant.routine(deps=["firmware.bin"])
def install():
	os.system("./install.sh")

licant.ex("firmware.bin")