import glink.util

class target:
	def __init__(self, context, tgt, deps, **kwargs):
		self.context = context
		self.depends = set()
		self.tgt = tgt

		for d in deps:
			self.depends.add(d)
		
		for k, v in kwargs.items():
			setattr(self, k, v)

	def invoke(self, func):
		if (isinstance(func ,str)):
			res = getattr(self, func, None)
			if (res == None):
				return None
			ret = res(self)
			return ret
		else:
			return func(self)

	def __repr__(self):
		return "target:"+self.tgt

class context:
	def __init__(self):
		self.targets={}
		self.unresolve_handlers=[]

	def virtual(self, tgt, deps):
		self.targets[tgt] = target(context=self, tgt=tgt, deps=deps)

	def get_target(self, tgt):
		if tgt in self.targets:
			return self.targets[tgt]
		
		for hndlr in self.unresolve_handlers:
			res = hndlr(self, tgt)
			if res:
				return self.targets[tgt]

		print("Попытка получить несуществующую цель: {0}".format(tgt))
		exit(-1)

	def add_unresolve_handler(self, hndlr):
		self.unresolve_handlers.append(hndlr)

	def depends_as_set(self, tgt, incroot=True):
		res = set()
		if incroot:
			res.add(tgt)
		
		target = self.get_target(tgt)
		
		for d in target.depends:
			#print(d)
			if not d in res:
				res.add(d)
				subres = self.depends_as_set(d)
				res = res.union(subres)
		return res

	def invoke_foreach(self, func):
		save = dict(self.targets)
		for k, v in save.items():
			v.invoke(func)

	def generate_rdepends_lists(self, targets):
		for t in targets:
			t.rdepends = []

		for t in targets:
			for dname in t.depends:
				dtarget = self.get_target(dname)
				dtarget.rdepends.append(t.tgt)


	def reverse_recurse_invoke(self, root, ops, cond=glink.util.always_true):
		depset = self.depends_as_set(root)
		targets_list = [self.get_target(t) for t in depset]
		sum = 0

		self.generate_rdepends_lists(targets_list)
		for t in targets_list:
			t.rcounter = 0

		works = glink.util.queue()

		for t in targets_list:
			if t.rcounter == len(t.depends):
				works.put(t)

		while(not works.empty()):
			w = works.get()

			if cond(self, w):
				ret = w.invoke(ops)
				if not (ret == 0 or ret == None):
					raise context.ResultIsNotNull()
				if ret == 0:
					sum += 1

			for r in [self.get_target(t) for t in w.rdepends]:
				r.rcounter = r.rcounter + 1
				if r.rcounter == len(r.depends):
					works.put(r)

		return sum

	def invoke_for_depends(self, root, ops, cond=None):
		depset = self.depends_as_set(root)
		sum = 0
		ret = None

		for d in depset:
			target = self.get_target(d)
			if cond==None:
				ret = target.invoke(ops)
			else:
				if cond(self, target):
					ret = target.invoke(ops)
			if ret == 0:
				sum+=1

		return sum


def as_list(src):
	if (not isinstance(src, list)):
		return [src]
	return src

class operations_chain:
	def __init__(self, lst):
		self.lst = lst 

	def __call__(self, target):
		for l in self.lst:
			ret = target.invoke(l)
			if ret != 0 and ret != None:
				return ret
		return 0