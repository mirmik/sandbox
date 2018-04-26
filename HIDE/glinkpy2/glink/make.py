import glink.core as core
import glink.cache
import os

def execute(target, rule, echo=False, message=None):
	rule = rule.format(**target.__dict__)

	if echo:
		print(rule)
	
	if message:
		print(self.message.format(**target.__dict__))

	ret = os.system(rule)
	return ret

class file_target(glink.core.target):
	def __init__(self, context, tgt, deps, **kwargs):
		glink.core.target.__init__(self, context, tgt, deps, **kwargs)
		self.isfile = True
		self.need = True

	def update_info(self, _self):
		context = self.context
		cache = context.fcache
		cache.update_info(self.tgt)

	def need_if_timestamp_compare(self, _self):
		context = self.context
		cache = context.fcache

		curinfo = cache.cache[self.tgt]
		curmtime = curinfo.mtime
		if curmtime == None:
			self.need = True
			return 0

		maxmtime = 0
		for dep in [context.get_target(t) for t in self.depends]:
			if dep.isfile:
				info = cache.cache[dep.tgt]
				if info.exist == False:
					return True
				if info.mtime > maxmtime:
					maxmtime = info.mtime

		if maxmtime > curmtime:
			self.need = True
		else:
			self.need = False

		return 0

	def need_if_exist(self, _self):
		context = self.context
		cache = context.fcache

		curinfo = cache.cache[self.tgt]
		if curinfo.exist:
			self.need = True
		else:
			self.need = False

		return 0

class executor:
	def __init__(self, rule, echo=False, message=None):
		self.rule = rule
		self.echo = echo
		self.message = message

	def __call__(self, target):
		return execute(target, self.rule, self.echo, self.message)

class make(core.context):
	def __init__(self):
		core.context.__init__(self)
		self.add_unresolve_handler(try_resolve_as_file)
		#self.add_unresolve_handler(try_resolve_as_function)
		self.fcache = glink.cache.fcache()

	def copy(self, src, tgt, echo=False, message=None, rmmsg=None):
		self.targets[tgt] = file_target(
			context=self,
			tgt=tgt, 
			act=executor("cp {src} {tgt}", echo, message),
			clr=executor("rm -f {tgt}", echo, rmmsg),  
			src=src,
			deps=[src]
		)

	#def rename(self, src, tgt, echo=False, message=None, rmmsg=None):
	#	self.add_target(
	#		tgt=tgt, 
	#		act=executor("mv {src} {tgt}", echo, message, checkneed=True),
	#		clr=executor("rm -f {tgt}", echo, rmmsg),
	#		src=src,
	#		isfile=True,
	#		deps=[src]
	#	)	

	def echo(self, tgt, msg, deps=[]):
		self.targets[tgt] = glink.core.target(
			context=self,
			tgt=tgt, 
			act=executor("echo {msg}"),
			msg=msg,
			deps=deps
		)	

	def file(self, tgt):
		self.targets[tgt] = file_target(context=self,tgt=tgt, deps=[])


	def directories_keeper(self, root):
		depset = self.depends_as_set(root)
		targets = [self.get_target(t) for t in depset]

		for target in targets:
			if isinstance(target, file_target):
				dr = os.path.normpath(os.path.dirname(target.tgt))
				if (not os.path.exists(dr)):
					print("MKDIR %s" % dr)
					os.mkdir(dr)

	def print_result_string(self, ret):
		if ret == 0:
			print(glink.util.yellow("Nothing to do"))
		else:
			print(glink.util.green("Success"))

	def clean(self, root):
		self.invoke_for_depends(root = root, ops = "update_info")
		self.invoke_for_depends(root = root, ops = "need_if_exist")
		return self.invoke_for_depends(root=root, ops="clr", cond=glink.make.if_need_or_not_file)

	def make(self, root):
		self.directories_keeper(root = root)
		self.invoke_for_depends(root = root, ops = "update_info")
		self.invoke_for_depends(root = root, ops = "need_if_timestamp_compare")
		self.reverse_recurse_invoke(root = root, ops = need_spawn)
		return self.reverse_recurse_invoke(root = root, ops = "act", cond = glink.make.if_need_or_not_file)
		
def try_resolve_as_file(cntxt, tgt):
	if os.path.exists(tgt):
		cntxt.file(tgt=tgt)
		return True
	return False

def if_need_or_not_file(context, target):
	if (not isinstance(target, file_target)):
		return True
	else:
		return target.need

def need_spawn(target):
	deptgts = [target.context.get_target(t) for t in target.depends]
	for dt in deptgts:
		if dt.need == True:
			target.need = True
			return 