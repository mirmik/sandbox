import sys
import os

class queue:
	class DontHaveArg:
		pass

	def __init__(self):
		self.lst = []
		self.rdr = 0

	def put(self, obj):
		self.lst.append(obj)

	def get(self):
		if (len(self.lst) == 0):
			raise DontHaveArg()

		ret = self.lst[self.rdr]

		self.rdr += 1 
		if self.rdr >= len(self.lst):
			self.__init__()

		return ret

	def empty(self):
		return len(self.lst) == 0

	def __str__(self):
		return str(self.lst)

def textblock(str):
	return chr(27) + str + chr(27) + "[0m"

def red(str):
	return textblock("[31;1m" + str)

def green(str):
	return textblock("[32;1m" + str)

def yellow(str):
	return textblock("[33;1m" + str)

def do_argv_routine(arg, default, locs):
	if len(sys.argv) <= arg:
		func = default
	else:
		func = sys.argv[arg]
	
	if func in locs:
		return locs[func]()
	else:
		print("Плохая рутина")
		exit(-1)



def always_true(context, work):
	return True

def changeext(path, newext):
	return os.path.splitext(path)[0]+"."+newext 