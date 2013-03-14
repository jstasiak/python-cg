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

	def __init__(self, bridge, cgparameter, name, semantic, type, base_type):
		self._bridge = bridge
		self._cgparameter = cgparameter

		#: Gets name of the parameter (string)
		self.name = name

		#: Gets type of the parameter (string)
		self.type = type

		#: Gets base type of the parameter (string)
		self.base_type = base_type

		#: Gets parameter semantic (string)
		self.semantic = semantic

		self.repr_members = ('name', 'semantic', 'type', 'base_type')
	
	def set_value(self, value):
		raise NotImplementedError()


class NumericParameter(Parameter):
	'''
	Represents numeric parameter (float, array of ints, matrix of doubles etc.).
	'''
	def __init__(self, row_count, column_count, **kwargs):
		super(NumericParameter, self).__init__(**kwargs)

		#: Gets parameter row count
		self.row_count = row_count

		#: Gets parameter column count
		self.column_count = column_count
		
		self.repr_members += ('row_count', 'column_count',)

	def set_value(self, value):
		'''
		Sets the parameter value. Value can be one of the following::

		* py:class:`numpy.ndarray` of `float32`, `float64` or `int32`. If the array
			is multidimensional, it will be reshaped to one dimension.
		* iterable of elements of type matching parameter type
		* scalar value of type matching parameter type

		.. note:: Setting parameter value is a slow operation and should be performed as
			rarely as possible.

		.. note:: Matrices will be filled with data in row-major order.
		'''

		if isinstance(value, ndarray):
			if value.ndim > 1:
				value = value.reshape(-1)

			letter = numpy_type_to_letter[value.dtype]
			method_name = 'cgSetParameterValue%sr' % (letter,)
			method = getattr(self._bridge, method_name)
			method(self._cgparameter, len(value), value)
		else:
			if not hasattr(value, '__iter__'):
				value = (value,)

			numpy_type = cg_type_to_numpy_type[self.base_type]
			array_value = array(value, dtype=numpy_type)
			self.set_value(array_value)

class SamplerParameter(Parameter):
	'''
	Represents sampler* parameter.
	'''
	def set_value(self, value):
		'''
		Sets sampler value.

		:param uint value: OpenGL texture object
		'''
		self._bridge.cgGLSetTextureParameter(self._cgparameter, value)
		self._bridge.cgSetSamplerState(self._cgparameter)


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
		type = self._bridge.cgGetParameterType(cgparameter)
		base_type = self._bridge.cgGetParameterBaseType(cgparameter)

		base_type_string=self._bridge.cgGetTypeString(base_type)
		type_string=self._bridge.cgGetTypeString(type)

		
		kwargs = dict(
			bridge=self._bridge,
			cgparameter=cgparameter,
			name=self._bridge.cgGetParameterName(cgparameter),
			type=type_string,
			base_type=base_type_string,
			semantic = self._bridge.cgGetParameterSemantic(cgparameter),
		)

		if type_string.startswith('sampler'):
			return SamplerParameter(**kwargs)
		elif base_type_string in cg_type_to_numpy_type:
			kwargs.update(dict(
				row_count=self._bridge.cgGetParameterRows(cgparameter),
				column_count=self._bridge.cgGetParameterColumns(cgparameter),
			))
			return NumericParameter(**kwargs)
		else:
			raise Error('Unsupported parameter type', base_type_string, type_string)

	def get_by_cgeffect(self, cgeffect):
		cgparameters = gather(
			cgeffect, self._bridge.cgGetFirstEffectParameter, self._bridge.cgGetNextParameter)

		return ParameterCollection(
			self.create_parameter_by_cgparameter(cgp) for cgp in cgparameters)
