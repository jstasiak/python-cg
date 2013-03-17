# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.effect.effect import Effect
from cg.utils import Disposable

class Context(Disposable):
	'''
	Wraps Cg context.
	'''

	def __init__(self, cgcontext, bridge):
		self._cgcontext = cgcontext
		self._bridge = bridge

	def perform_dispose(self):
		self._bridge.cgDestroyContext(self._cgcontext)

	def create_effect_from_file(self, filename):
		'''
		Loads effect source from file and creates effect using it.

		:param string filename: file containing effect source.
		:rtype: :py:class:`cg.effect.effect.Effect`
		'''
		cgeffect = self._bridge.cgCreateEffectFromFile(self._cgcontext, filename)
		return Effect(cgeffect, self._bridge)

	def create_effect(self, source):
		'''
		Creates effect from source.

		:param string source: effect source
		:rtype: :py:class:`cg.effect.effect.Effect`
		'''
		cgeffect = self._bridge.cgCreateEffect(self._cgcontext, source)
		return Effect(cgeffect, self._bridge)

	def get_last_listing(self):
		return self._bridge.cgGetLastListing(self._cgcontext)

	@property
	def manage_texture_parameters(self):
		'''
		Gets and sets whether Cg is supposed to automatically manage (enable/disable) texture
		parameters (bool).
		'''
		return self._bridge.cgGLGetManageTextureParameters(self._cgcontext)

	@manage_texture_parameters.setter
	def manage_texture_parameters(self, value):
		self._bridge.cgGLSetManageTextureParameters(self._cgcontext, value)

	def register_states(self):
		'''
		Register graphics API states for use in effects.

		.. note:: This method is idempotent.
		'''
		self._bridge.cgGLRegisterStates(self._cgcontext)


class ContextFactory(object):
	def __init__(self, bridge):
		self._bridge = bridge

	def create(self):
		cgcontext = self._bridge.cgCreateContext()
		return Context(cgcontext, self._bridge)
