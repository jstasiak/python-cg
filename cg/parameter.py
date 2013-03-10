# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from numpy import array, dtype, ndarray

from cg.errors import Error
from cg.utils import autoassign, gather, ReprMixin

numpy_type_to_letter = dict((dtype(key), value) for (key, value) in (
	('float32', 'f'),
	('float64', 'd'),
	('int32', 'i'),
))

cg_type_to_numpy_type = dict(
	(key, dtype(value)) for (key, value) in (
		('float', 'float32'),
		('fixed', 'float32'),
		('half', 'float32'),
		('double', 'float64'),
		('bool', 'int32'),
		('int', 'int32'),
	)
)

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

		#: Gets parameter semantic (string)
		self.semantic = semantic

	def set_value(self, value):
		'''
		Sets the parameter value. Value can be one of the following::

		* one dimenstional py:class:`numpy.ndarray` of `float32`, `float64` or `int32`
		* iterable of elements of type matching parameter type
		* scalar value of type matching parameter type

		.. note:: Setting parameter value is a slow operation and should be performed as
			rarely as possible.
		'''

		if isinstance(value, ndarray):
			letter = numpy_type_to_letter[value.dtype]
			method_name = 'cgSetParameterValue%sc' % (letter,)
			method = getattr(self._bridge, method_name)
			method(self._cgparameter, len(value), value)
		else:
			if not hasattr(value, '__iter__'):
				value = (value,)

			numpy_type = cg_type_to_numpy_type[self.base_type]
			array_value = array(value, dtype=numpy_type)
			self.set_value(array_value)


class ParameterCollection(tuple):
	'''
	Collection of :py:class:`cg.parameter.Parameter`. Provides tuple interface (iteration,
	indexing etc.) and some parameter-specific extensions.
	'''

	@property
	def by_semantic(self):
		'''
		Gets parameter dictionary indexed by semantic. Only parameters with
		non-empty semantic are included.
		'''
		return dict((p.semantic, p) for p in self if p.semantic)

	@property
	def by_name(self):
		'''
		Gets parameter dictionary indexed by names.
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

		if type_string in ('struct',) or \
				type_string.startswith('sampler') or \
				base_type_string not in cg_type_to_numpy_type:
			raise Error('Unsupported parameter type', base_type_string, type_string)

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
