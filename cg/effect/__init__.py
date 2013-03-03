# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.effect.technique import Technique
from cg.utils import Disposable, gather

class Effect(Disposable):
	'''
	Wraps CG Effect.
	'''

	_techniques = None

	def __init__(self, cgeffect, bridge):
		self._cgeffect = cgeffect
		self._bridge = bridge

	@property
	def techniques(self):
		'''
		Gets techniques defined for an effect as a tuple of
		:py:class:`cg.effect.technique.Technique`.
		'''
		if self._techniques is None:
			self._techniques = tuple(
				Technique(cg_technique, self._bridge) for cg_technique in gather(
					self._cgeffect,
					self._bridge.cgGetFirstTechnique, self._bridge.cgGetNextTechnique
				)
			)

		return self._techniques

	def perform_dispose(self):
		self._bridge.cgDestroyEffect(self._cgeffect)
