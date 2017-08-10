import os

class executor:
	def __init__(self, rule, echo=False, message=None):
		self.rule = rule
		self.echo = echo
		self.message = message

	def __call__(self, target):
		rule = self.rule.format(**target.__dict__)
		#print(rule)

		if self.echo:
			print(rule)
	
		if self.message:
			print(self.message.format(**target.__dict__))

		return os.system(rule)


class target:
	def __init__(self, tgt, deps, **kwargs):
		self.depends = set()
		self.tgt = tgt

		for d in deps:
			self.depends.add(d)
		
		for k, v in kwargs.items():
			setattr(self, k, v)

	def invoke(self, func):
		getattr(self, func)(self)

class context:
	def __init__(self):
		self.targets={}
		self.unresolve_handler=None

	def add_target(self, tgt, deps, **kwargs):
		self.targets[tgt] = target(tgt, deps, **kwargs)

	def copy(self, src, tgt, echo=False, message=None):
		self.add_target(
			tgt=tgt, 
			act=executor("cp {src} {tgt}", echo, message), 
			src=src,
			isfile=True,
			deps=[src]
		)	

	def rename(self, src, tgt, echo=False, message=None):
		self.add_target(
			tgt=tgt, 
			act=executor("mv {src} {tgt}", echo, message), 
			src=src,
			isfile=True,
			deps=[src]
		)	

	def get_target(self, tgt):
		if tgt in self.targets:
			return self.targets[tgt]
		
		if self.unresolve_handler:
			res = self.unresolve_handler(self, tgt)
			if res:
				return self.targets[tgt]

		print("Попытка получить несущесвыющую цель: {0}".format(tgt))
		exit(-1)

	def set_unresolve_handler(self, hndlr):
		self.unresolve_handler = hndlr

	def depends_as_set(self, tgt):
		res = set()
		target = self.get_target(tgt)
		
		for d in target.depends:
			#print(d)
			if not d in res:
				res.add(d)
				subres = self.depends_as_set(d)
				res = res.union(subres)
		return res

def try_resolve_as_file(cntxt, tgt):
	if os.path.exists(tgt):
		cntxt.add_target(tgt=tgt, deps=[], isfile=True)
		return True
	return False


#def executor(str, trans, echo=False, message=None):
#	if echo:
#		print(str)
#	
#	if message:
#		print(message.format(tgt=trans.tgt))
#
#	return os.system(str)
#
#def always_true(self):
#		return True
#
#def src_as_dep(self):
#	return self.src
#
#def quite_remove(self):
#	return os.system("rm {tgt} || true".format(tgt=self.tgt))
#
#def if_deps_is_exists(self):
#	for d in self.dep(self):
#		if os.path.exists(d) == False:
#			return False
#	return True
#
#def copy_action(self, **kwargs):
#		if (len(self.src) != 1):
#			print("src can't to be list")
#			exit(-1)
#
#		return executor("cp {src} {tgt}".format(src=self.src[0], tgt=self.tgt), self, **kwargs)
#
#		#return os.system("cp {src} {tgt}".format(src=self.src[0], tgt=self.tgt))
#
#class context:
#
#	endpoints = {}
#	translations = {}
#
#	class endpoint:
#		def __init__(self, tgt, chk):
#			self.tgt = tgt
#			self.chk = chk
#
#		def check(self):
#			return self.chk(self)
#
#	class translation:
#		def __init__(self, src, tgt, act, chk, dep, rem):
#			self.src = src
#			self.tgt = tgt
#			self.act = act
#			self.chk = chk
#			self.dep = dep
#			self.rem = rem
#
#		def check(self):
#			return self.chk(self)
#
#		def depends(self):
#			return self.dep(self)
#
#		def remove(self):
#			return self.rem(self)
#
#		def do_action(self, **kwargs):
#			return self.act(self, **kwargs)
#
#
#	def add_trans(self, src, tgt, act, 
#		chk=always_true, 
#		dep=src_as_dep,
#		rem=quite_remove
#	):
#		trans = context.translation(as_list(src), tgt, act, chk, dep, rem)
#		self.translations[tgt] = trans
#
#	def add_virtual(self, src, tgt, act, chk=always_true, dep=src_as_dep):
#		virt = context.virtual(src, tgt, act, chk, dep)
#		self.virtuals[tgt] = virt
#
#	def add_endpoint(self, tgt, chk):
#		ep = context.endpoint(tgt, chk)
#		self.endpoints[tgt] = ep
#
#	def clean_translations(self):
#		for k in self.translations:
#			self.translations[k].remove()
#
#
#	def copy(self, src, tgt):
#		self.add_trans(src, tgt, 
#			act=copy_action, 
#			chk=if_deps_is_exists, 
#			dep=src_as_dep
#		)
#
#	def execute(self):
#		print("execute")

def as_list(src):
	if (not isinstance(src, list)):
		return [src]
	return src