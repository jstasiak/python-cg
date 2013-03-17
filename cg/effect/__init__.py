# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.parameter import EffectParameterFactory
from cg.effect.technique import EffectTechniqueFactory
from cg.utils import Disposable, gather

class Effect(Disposable):
	'''
	Wraps CG Effect.
	'''

	_parameters = None
	_techniques = None

	def __init__(self, cgeffect, bridge, parameter_factory=None, technique_factory=None):
		self._cgeffect = cgeffect
		self._bridge = bridge
		self._parameter_factory = parameter_factory or EffectParameterFactory(self._bridge)
		self._technique_factory = technique_factory or EffectTechniqueFactory(self._bridge)

	@property
	def techniques(self):
		'''
		Gets techniques defined for an effect as a tuple of
		:py:class:`cg.effect.technique.EffectTechnique`.
		'''
		if self._techniques is None:
			self._techniques = self._technique_factory.get_by_cgeffect(self._cgeffect)

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
