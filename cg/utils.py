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
