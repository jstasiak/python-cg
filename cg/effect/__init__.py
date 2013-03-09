# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.parameter import EffectParameterFactory
from cg.effect.technique import Technique
from cg.utils import Disposable, gather

class Effect(Disposable):
	'''
	Wraps CG Effect.
	'''

	_parameters = None
	_techniques = None

	def __init__(self, cgeffect, bridge, parameter_factory=None):
		self._cgeffect = cgeffect
		self._bridge = bridge
		self._parameter_factory = parameter_factory or EffectParameterFactory(self._bridge)

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

	@property
	def parameters(self):
		'''
		Gets effect parameters as a :py:class:`cg.parameter.ParameterCollection`.
		'''
		if self._parameters is None:
			self._parameters = self._parameter_factory.get_by_cgeffect(self._cgeffect)

		return self._parameters

	def perform_dispose(self):
		self._bridge.cgDestroyEffect(self._cgeffect)
