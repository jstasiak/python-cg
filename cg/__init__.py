# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from cg import bridge

class Context:

	def __init__(self, cgcontext):
		self._cgcontext = cgcontext

	def __del__(self):
		bridge.cgDestroyContext(self._cgcontext)

	def create_effect_from_file(self, filename):
		cgeffect = bridge.cgCreateEffectFromFile(self._cgcontext, filename)
		return Effect(cgeffect)

	def get_last_listing(self):
		return bridge.cgGetLastListing(self._cgcontext)

class Effect(object):
	_techniques = None

	def __init__(self, cgeffect):
		self._cgeffect = cgeffect

	@property
	def techniques(self):
		if self._techniques is None:
			techniques = []
			technique = bridge.cgGetFirstTechnique(self._cgeffect)
			while technique:
				techniques.append(Technique(technique))
				technique = bridge.cgGetNextTechnique(technique)
			self._techniques = tuple(techniques)

		return self._techniques

class Technique(object):
	_passes = None

	def __init__(self, cgtechnique):
		self._cgtechnique = cgtechnique

	@property
	def passes(self):
		if self._passes is None:
			passes = []
			pass_ = bridge.cgGetFirstPass(self._cgtechnique)
			while pass_:
				passes.append(Pass(pass_))
				pass_ = bridge.cgGetNextPass(pass_)

			self._passes = tuple(passes)
		return self._passes

class Pass(object):
	def __init__(self, cgpass):
		self._cgpass = cgpass

	def begin(self):
		bridge.cgSetPassState(self._cgpass)
	
	def end(self):
		bridge.cgResetPassState(self._cgpass)

class ContextFactory(object):
	def create(self):
		cgcontext = bridge.cgCreateContext()
		bridge.cgGLRegisterStates(cgcontext)
		return Context(cgcontext)
