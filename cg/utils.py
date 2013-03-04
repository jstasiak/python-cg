# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractmethod
from functools import wraps

WithABCMeta = ABCMeta(str('WithABCMeta'), (object,), {})

class Disposable(WithABCMeta):
	'''
	Exposes method to release resources held by the class.
	'''

	_disposed = False

	def dispose(self):
		'''
		Disposes of resources that are owned by the object.
		
		.. note:: This method is idempotent.
		'''
		if not self._disposed:
			self.perform_dispose()
			self._disposed = True

	@abstractmethod
	def perform_dispose(self):
		'''
		Performs actual disposing, needs to be overridden by a subclass.

		.. note:: This method is not supposed to be called directly by the user code. Please
			use :py:meth:`dispose` instead.
		'''

	def __del__(self):
		self.dispose()

def gather(owner, get_first, get_next):
	elements = []

	current = get_first(owner)
	while current:
		elements.append(current)
		current = get_next(current)

	return tuple(elements)

def nativerepr(repr_function):
	'''
	__repr__ decorator that makes sure __repr__ returns result of the right type (byte string
	for Python 2.x, (unicode) string for Python 3). Performs conversion from unicode to byte
	string when necessary.
	'''
	@wraps(repr_function)
	def wrapper(self):
		result = repr_function(self)
		if str is not bytes:
			assert isinstance(result, str), 'Always return (unicode) string from __repr__'
		else:
			assert isinstance(result, basestring)
			if not isinstance(result, str):
				result = result.encode('utf-8')

		return result
	
	return wrapper

def autoassign(function):
	'''
	Decorator for instance methods, copies all keyword arguments to instance members
	and then calls the decorated method passing all the parameters.

	.. note:: Decorated method accepts only keyword arguments.
	'''
	@wraps(function)
	def wrapper(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
		return function(self, **kwargs)
	return wrapper
