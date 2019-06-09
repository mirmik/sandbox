#!/usr/bin/env python3
#coding: utf-8

import licant

licant.libs.include("linalg-v3")
licant.libs.include("gxx")

licant.cxx_application("target",
	sources=["main.cpp"],
	mdepends=["linalg-v3", "gxx"],	
)

licant.ex("target")