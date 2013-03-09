# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.utils import autoassign, gather, ReprMixin

class Parameter(ReprMixin):
	'''
	Effect or program parameter base class.
	'''

	repr_members = ('name', 'semantic', 'type', 'base_type', 'row_count', 'column_count')

	def __init__(self, bridge, cgparameter, name, semantic,
			type, base_type, row_count, column_count):
		self._bridge = bridge
		self._cgparameter = cgparameter

		#: Gets name of the parameter (string)
		self.name = name

		#: Gets type of the parameter (string)
		self.type = type

		#: Gets base type of the parameter (string)
		self.base_type = base_type

		#: Gets parameter row count
		self.row_count = row_count

		#: Gets parameter column count
		self.column_count = column_count

		#: Gets parameter semantic
		self.semantic = semantic

	def set_value_fc(self, data):
		self._bridge.cgSetParameterValuefc(self._cgparameter, len(data), data)

class ParameterCollection(tuple):
	@property
	def by_semantic(self):
		'''
		Returns parameter dictionary indexed by semantic. Only parameters with
		non-empty semantic are included.
		'''
		return dict((p.semantic, p) for p in self if p.semantic)

	@property
	def by_name(self):
		'''
		Returns parameter dictionary indexed by names.
		'''
		return dict((p.name, p) for p in self)

class EffectParameterFactory(object):
	def __init__(self, bridge):
		self._bridge = bridge

	def create_parameter_by_cgparameter(self, cgparameter):
		name = self._bridge.cgGetParameterName(cgparameter)
		type = self._bridge.cgGetParameterType(cgparameter)
		base_type = self._bridge.cgGetParameterBaseType(cgparameter)

		type_string = self._bridge.cgGetTypeString(type)
		base_type_string = self._bridge.cgGetTypeString(base_type)

		row_count = self._bridge.cgGetParameterRows(cgparameter)
		column_count = self._bridge.cgGetParameterColumns(cgparameter)

		semantic = self._bridge.cgGetParameterSemantic(cgparameter)

		return Parameter(bridge=self._bridge,
			cgparameter=cgparameter,
			name=name,
			type=type_string,
			semantic=semantic,
			base_type=base_type_string,
			row_count=row_count,
			column_count=column_count)

	def get_by_cgeffect(self, cgeffect):
		cgparameters = gather(
			cgeffect, self._bridge.cgGetFirstEffectParameter, self._bridge.cgGetNextParameter)

		return ParameterCollection(
			self.create_parameter_by_cgparameter(cgp) for cgp in cgparameters)
