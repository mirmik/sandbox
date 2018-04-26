#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append('./..')

import glink.base as gl
import glink.cpp

cntxt = glink.base.Context()

#gl = glink.base.GlinkContext()

#mo = cpp.Object(cpp.Source("main.cpp"), [cpp.Header("main.h")])

#mo.execute_action()


#def html_builder:
#html = html_builder('main.c')

cntxt.env["BUILD"] = "build"

cp_builder = gl.FileBuilder(
	rule = "cp {srcs} {tgt}",
)

cp = cp_builder(tgt = "copy", src = "first")

cp.execute_action(cntxt, echo = True)