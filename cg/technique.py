# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class Technique(object):
	_passes = None

	def __init__(self, cgtechnique, bridge):
		self._cgtechnique = cgtechnique
		self._bridge = bridge

	@property
	def passes(self):
		if self._passes is None:
			passes = []
			pass_ = self._bridge.cgGetFirstPass(self._cgtechnique)
			while pass_:
				passes.append(Pass(pass_, self._bridge))
				pass_ = self._bridge.cgGetNextPass(pass_)

			self._passes = tuple(passes)
		return self._passes

class Pass(object):
	def __init__(self, cgpass, bridge):
		self._cgpass = cgpass
		self._bridge = bridge

	def begin(self):
		self._bridge.cgSetPassState(self._cgpass)
	
	def end(self):
		self._bridge.cgResetPassState(self._cgpass)
