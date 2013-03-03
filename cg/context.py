# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.effect import Effect
from cg.utils import Disposable

class Context(Disposable):
	'''
	Wraps CG Toolkit Context.
	'''

	def __init__(self, cgcontext, bridge):
		self._cgcontext = cgcontext
		self._bridge = bridge

	def perform_dispose(self):
		self._bridge.cgDestroyContext(self._cgcontext)

	def create_effect_from_file(self, filename):
		cgeffect = self._bridge.cgCreateEffectFromFile(self._cgcontext, filename)
		return Effect(cgeffect, self._bridge)

	def get_last_listing(self):
		return self._bridge.cgGetLastListing(self._cgcontext)


class ContextFactory(object):
	def __init__(self, bridge):
		self._bridge = bridge

	def create(self):
		cgcontext = self._bridge.cgCreateContext()
		self._bridge.cgGLRegisterStates(cgcontext)
		return Context(cgcontext, self._bridge)
