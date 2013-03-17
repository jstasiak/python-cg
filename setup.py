#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import platform

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from distutils.extension import Extension
from os import environ

import numpy
from Cython.Distutils import build_ext

if platform.system() == 'Darwin':
	environ['LDFLAGS']='-framework Cg'
	libraries=[]
else:
	libraries=['Cg', 'CgGL', 'GL']
	
extensions = [
	Extension(
		"cg.bridge",
		["cg/bridge.pyx"],
		libraries=libraries,
		include_dirs=['cg'],
	)
]

setup(
	name='python-cg',
	version='0.1',
	description='Python wrapper for NVidia Cg Toolkit',
	author='Jakub Stasiak',
	author_email='jakub@stasiak.at',
	packages=['cg'],
	cmdclass={'build_ext': build_ext},
	ext_modules=extensions,
	requires=[
		'cython (>= 0.18)',
	],
	include_dirs=[numpy.get_include()]
)
