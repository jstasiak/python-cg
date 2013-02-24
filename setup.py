#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform

from distutils.core import setup
from distutils.extension import Extension
from os import environ


from Cython.Distutils import build_ext

if platform.system() == 'Darwin':
	environ['LDFLAGS']='-framework Cg'
	libraries=[]
else:
	libraries=['Cg', 'CgGL', 'GL']
	
extensions = [
	Extension(
		"cg.bridge",
		["src/bridge.pyx"],
		libraries=libraries,
	)
]

setup(
	name='python-cg',
	version='0.1',
	description='Python wrapper for NVidia Cg Toolkit',
	author='Jakub Stasiak',
	author_email='jakub@stasiak.at',
	package_dir=dict(cg='src'),
	cmdclass={'build_ext': build_ext},
	ext_modules=extensions,
	requires=[
		'cython',
		'nose',
	],
)
