# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg import bridge as cbridge
from cg.effect import Effect

class Context:
	def __init__(self, cgcontext, bridge):
		self._cgcontext = cgcontext
		self._bridge = bridge

	def __del__(self):
		self._bridge.cgDestroyContext(self._cgcontext)

	def create_effect_from_file(self, filename):
		cgeffect = self._bridge.cgCreateEffectFromFile(self._cgcontext, filename)
		return Effect(cgeffect, self._bridge)

	def get_last_listing(self):
		return self._bridge.cgGetLastListing(self._cgcontext)


class ContextFactory(object):
	def __init__(self, bridge=None):
		if bridge is not None:
			self._bridge = bridge
		else:
			self._bridge = cbridge

	def create(self):
		cgcontext = self._bridge.cgCreateContext()
		self._bridge.cgGLRegisterStates(cgcontext)
		return Context(cgcontext, self._bridge)
