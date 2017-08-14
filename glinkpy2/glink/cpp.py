import glink.make
import os

class binutils:
	def __init__(self, cxx, cc, ld, ar, objdump):
		self.cc = cc
		self.cxx = cxx
		self.ld = ld
		self.ar = ar
		self.objdump = objdump

cxx_ext_list = ["cpp", "cxx"]
cc_ext_list = ["cc", "c"]
asm_ext_list = ["asm", "s", "S"]

class cpp_maker(glink.make.make):
	def __init__(self, binutils):
		glink.make.make.__init__(self)
		self.binutils = binutils

	def object(self, src, tgt, type=None, echo=True, message=None, rmmsg=None):
		if type == None:
			ext = src.split('.')[-1]
		
			if ext in cxx_ext_list:
				type = "cxx"
			elif ext in cc_ext_list:
				type = "cc"
			elif ext in asm_ext_list:
				type = "asm"
			else:
				print(glink.util.red("Unrecognized extention"))
				exit(-1)

		if type == "cxx":
			act = glink.make.executor("{context.binutils.cxx} -c {src} -o {tgt}", echo, message)
		elif type == "cc":
			act = glink.make.executor("{context.binutils.cc} -c {src} -o {tgt}", echo, message)
		elif type == "asm":
			act = glink.make.executor("{context.binutils.cc} -c {src} -o {tgt}", echo, message)

		else:
			print(glink.util.red("Unrecognized extention"))
			exit(-1)


		self.targets[tgt] = glink.make.file_target(
			context=self,
			tgt=tgt, 
			src=src,
			deps=[src],
			act=act,
			clr=glink.make.executor("rm -f {tgt}", echo, rmmsg),  
		)

	def executable(self, tgt, srcs, echo=True, message=None, rmmsg=None):
		self.targets[tgt] = glink.make.file_target(
			context=self,
			tgt=tgt, 
			act=glink.make.executor("{context.binutils.cxx} {srcs} -o {tgt}", echo, message),
			clr=glink.make.executor("rm -f {tgt}", echo, rmmsg),  
			srcs=" ".join(srcs),
			deps=srcs
		)
		
def host_cxx_maker(**kwargs):
	cpp = cpp_maker(
		binutils(
			cxx= 		"c++",
			cc= 		"cc",
			ld= 		"ld",
			ar= 		"ar",
			objdump= 	"objdump"
		),
		**kwargs
	)
	return cpp
	
def avr_cxx_maker(**kwargs):
	cpp = cpp_maker(
		binutils(
			cxx= 		"avr-g++",
			cc= 		"avr-gcc",
			ld= 		"avr-ld",
			ar= 		"avr-ar",
			objdump= 	"avr-objdump"
		),
		**kwargs
	)
	return cpp