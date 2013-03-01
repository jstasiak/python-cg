# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.utils import gather

class Technique(object):
	_passes = None

	def __init__(self, cgtechnique, bridge):
		self._cgtechnique = cgtechnique
		self._bridge = bridge

	@property
	def passes(self):
		if self._passes is None:
			self._passes = tuple(Pass(cg_pass, self._bridge) for cg_pass in gather(
				self._cgtechnique, self._bridge.cgGetFirstPass, self._bridge.cgGetNextPass))

		return self._passes

class Pass(object):
	def __init__(self, cgpass, bridge):
		self._cgpass = cgpass
		self._bridge = bridge

	def begin(self):
		self._bridge.cgSetPassState(self._cgpass)
	
	def end(self):
		self._bridge.cgResetPassState(self._cgpass)
