# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.utils import Disposable, gather
from cg.technique import Technique

class Effect(Disposable):
	_techniques = None

	def __init__(self, cgeffect, bridge):
		self._cgeffect = cgeffect
		self._bridge = bridge

	@property
	def techniques(self):
		if self._techniques is None:
			self._techniques = gather(
				self._cgeffect,
				self._bridge.cgGetFirstTechnique, self._bridge.cgGetNextTechnique
			)

		return self._techniques

	def _dispose(self):
		self._bridge.cgDestroyEffect(self._cgeffect)
