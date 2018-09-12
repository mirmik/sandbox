#!/usr/bin/python3
#coding: utf-8

import licant
from licant.cxx_modules import application
from licant.libs import include
from licant.cxx_make import make_gcc_binutils

import os

include("genos")
include("gxx")
include("crow")
binutils = make_gcc_binutils("avr")

application("main", 
	binutils = binutils,
	sources = ["main.c"],
	target = "firmware.bin",

	cxx_flags = "-Os -fpermissive -fno-threadsafe-statics -flto",
	cc_flags = "-Os -flto",

	include_modules = [
		("genos"),
		("genos.board", "arduino_mega"),

		
		("genos.irqtbl"),
		("genos.tasklet"),
		("genos.timer"),
		("genos.schedee"),
		("gxx.syslock", "genos.atomic"),
		("genos.malloc", "lin"),
		
		("gxx.libc"),
		("gxx.std"),
		("gxx.posix"),

		("gxx.include"),
		("gxx.util"),
#		("gxx.log2", "stub"),
		
		("gxx.diag", "impl"),
		("gxx.dprint", "diag"),
		("gxx.print", "dprint"),

		("gxx.panic", "abort"),

		("crow"),
		("crow.allocator", "malloc"),

		("genos.chardev"),
		("genos.fs"),
	]
)

@licant.routine
def install():
	#os.system("sudo avrdude -P/dev/ttyUSB0 -v -cwiring -patmega2560 -b115200 -D -Uflash:w:./firmware.bin -u")
	os.system("sudo avrdude -P/dev/ttyUSB0 -v -cwiring -patmega2560 -b115200 -D -Uflash:w:./firmware.bin -u")

@licant.routine
def terminal():
	os.system("sudo gtkterm -p /dev/ttyUSB0 -s 115200")




#print(licant.core.core.get("build/__LOCAL_HEADERS__/__local__/arch_gpio.h").__dict__)
#exit(0)

licant.ex(default = "main", colorwrap = True)
