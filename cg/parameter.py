# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.utils import autoassign, gather, nativerepr

class Parameter(object):
	'''
	Effect or program parameter base class.
	'''

	def __init__(self, bridge, cgparameter, name):
		self._bridge = bridge
		self._cgparameter = cgparameter

		#: Name of the parameter
		self.name = name

	def set_value_fc(self, data):
		self._bridge.cgSetParameterValuefc(self._cgparameter, len(data), data)

	@nativerepr
	def __repr__(self):
		return '%s(name=%r)' % (self.__class__.__name__, self.name,)

class EffectParameterFactory(object):
	def __init__(self, bridge):
		self._bridge = bridge

	def create_parameter_by_cgparameter(self, cgparameter):
		name = self._bridge.cgGetParameterName(cgparameter)
		type = self._bridge.cgGetParameterType(cgparameter)
		base_type = self._bridge.cgGetParameterBaseType(cgparameter)

		type_string = self._bridge.cgGetTypeString(type)
		base_type_string = self._bridge.cgGetTypeString(base_type)

		rows = self._bridge.cgGetParameterRows(cgparameter)
		columns = self._bridge.cgGetParameterColumns(cgparameter)

		return Parameter(bridge=self._bridge, cgparameter=cgparameter, name=name)

	def get_by_cgeffect(self, cgeffect):
		cgparameters = gather(
			cgeffect, self._bridge.cgGetFirstEffectParameter, self._bridge.cgGetNextParameter)

		return tuple(self.create_parameter_by_cgparameter(cgp) for cgp in cgparameters)
