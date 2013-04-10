#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import absolute_import, division, print_function

import platform

from setuptools import Extension, setup

from os import environ, getcwd

try:
	import numpy
	include_dirs = [numpy.get_include()]
except ImportError:
	include_dirs = []

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
		['cg/bridge.' + ('pyx' if use_cython else 'c')],
		libraries=libraries,
		include_dirs=['cg'],
	)
]

setup(
	name='python-cg',
	version='0.1.3',
	description='Python wrapper for NVidia Cg Toolkit',
	author='Jakub Stasiak',
	author_email='jakub@stasiak.at',
	url='https://github.com/jstasiak/python-cg',
	platforms=['unix', 'linux', 'os x'],
	license='MIT',
	packages=['cg', 'cg.effect'],
	cmdclass=cmdclass,
	ext_modules=extensions,
	install_requires=[
		'numpy',
	],
	include_dirs=include_dirs,
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: Implementation :: CPython',
		'Topic :: Multimedia :: Graphics :: 3D Rendering',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
