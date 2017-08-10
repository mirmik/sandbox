import os
from glink.cache import Cache as Cache

class OptionsReaderGenerator:
	pass

class Environment(OptionsReaderGenerator):
	def get_options(self, context):
		return context.env

class Context:
	def __init__(self):
		self.env = {}
		self.targets = {}
		self.cache = Cache()

	def build(self, target):
		print("build target: {0}".format(target))
		#target.execute_action(self)

class Target:
	def __init__(self, name, action = None, options = None):
		self.name = name
		self.action = action
		self.options = options

	def execute_action(self, cntxt, echo = False):
		ret = self.action(self, self.options.get_options(cntxt), echo = echo)
		return ret

class GeneratedFile(Target):
	def __init__(self, sources, path, action, options):
		Target.__init__(self, name = path, action = action, options = options)
		self.sources = sources
		self.target = path
		self.depends = self.sources 

	def is_correct(self):
		pass

class FileBuilder:
	def __init__(self, rule, tgtgen = None):
		self.action = RuleAction(rule)
		#self.tgtgen = tgtgen

	def __call__(self, src = None, tgt = None, options = Environment()):
		src = as_list(src)

		#if (not tgt):
		#	tgt = self.tgtgen(src)

		target = GeneratedFile(
			sources = src, 
			path = tgt, 
			action = self.action, 
			options = options
		) 

		return target

def RuleAction(g_rule):
	def action(target, dict, echo = False, message = None):
		srcs = str.join(' ', target.sources)
		tgt = target.target
		rule = g_rule

		rule = rule.format(tgt = tgt, srcs = srcs)
		rule = rule.format(**dict)

		if (echo):
			print(rule)

		ret = os.system(rule)

		return ret
	return action


def as_list(lst):
	if (isinstance(lst, list)):
		return lst
	else:
		return [lst]