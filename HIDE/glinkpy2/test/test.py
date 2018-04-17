#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("..")

print(sys.path)

import glink.cpp
import glink.util as gu
print(glink.util.green("Script start"))

cpp = glink.cpp.host_cxx_maker()

srcs = [
	"main.cpp", 
	"ttt.cpp"
]

objs = ["build/main/" + gu.changeext(s,"o") for s in srcs]

for s, o in zip(srcs, objs):
    cpp.object(src=s, tgt=o)

cpp.executable(tgt="target", srcs=objs)

target = "target"

def all():
	return cpp.make(target)

def clean():
	return cpp.clean(target)

result = glink.util.do_argv_routine(arg=1, default="all", locs=locals())
cpp.print_result_string(result)