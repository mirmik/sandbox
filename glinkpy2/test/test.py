#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("..")

import glink.core

gl = glink.core.context()

gl.copy(src="first", tgt="second", echo=True)
gl.copy(src="second", tgt="third", echo=True)

gl.set_unresolve_handler(glink.core.try_resolve_as_file)
print(gl.depends_as_set("third"))

#print(gl.get_target("forth"))

#gl.translations["second"].do_action(message = "COPY {tgt}")
#gl.translations["third"].do_action(message = "COPY {tgt}")

#gl.targets["second"].invoke("act")
#gl.targets["third"].invoke("act")

#gl.clean_translations()

#gl.execute()

#gl.clean_translations()