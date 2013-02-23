#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform

from distutils.core import setup
from distutils.extension import Extension
from os import environ


from Cython.Distutils import build_ext

extensions = [
	Extension("cg.bridge", ["cg/bridge.pyx"]),
]

if platform.system() == 'Darwin':
	environ['LDFLAGS'] = '-framework Cg'

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
		'cython',
		'nose',
	],
)
