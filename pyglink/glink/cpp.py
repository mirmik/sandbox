import glink.base as base

#class Object(base.Target):
#	def __init__(self, source, headers):
#		self.source = source
#		self.headers = headers
#		self.depends.append(source)
#		self.depends.extend(headers)
#
#	def __repr__(self):
#		return self.depends
#
#class Source(base.Target):
#	#path = None
#
#	def __init__(self, path):
#		self.path = path
#
#	def __repr__(self):
#		return self.path
#
#	def __str__(self):
#		return "cppsrc({0})".format(self.path)
#
#class Header(base.Target):
#	#path = None
#
#	def __init__(self, path):
#		self.path = path
#
#	def __repr__(self):
#		return self.path
#
#	def __str__(self):
#		return "cppsrc({0})".format(self.path)
#
#
#class StaticLibrary(base.Target):
#	#path = None
#
#	def __init__(self, objs):
#		self.path = path
#
#	def __repr__(self):
#		return self.path
#
#	def __str__(self):
#		return "cppsrc({0})".format(self.path)
#
#class Executable(base.Target):
#	#path = None
#	def __init__(self, objs):
#		self.objects = objs
#
#	def __repr__(self):
#		return self.path
#
#	def __str__(self):
#		return "cppsrc({0})".format(self.path)
#