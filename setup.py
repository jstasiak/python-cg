#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import platform

from setuptools import setup

from distutils.extension import Extension
from os import environ

import numpy

cmdclass = {}

try:
	from Cython.Distutils import build_ext
	use_cython = True
	cmdclass['build_ext'] = build_ext
except ImportError:
	use_cython = False


if platform.system() == 'Darwin':
	environ['LDFLAGS']='-framework Cg'
	libraries=[]
else:
	libraries=['Cg', 'CgGL', 'GL']
	
extensions = [
	Extension(
		'cg.bridge',
		['cg/bridge.' + 'pyx' if use_cython else 'c'],
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
	cmdclass=cmdclass,
	ext_modules=extensions,
	install_requires=[
		'numpy',
	],
	include_dirs=[numpy.get_include()]
)
