# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractmethod

WithABCMeta = ABCMeta(str('WithABCMeta'), (object,), {})

class Disposable(WithABCMeta):
	'''
	Exposes method to release resources held by the class.
	'''

	_disposed = False

	def dispose(self):
		'''
		Disposes of resources that are owned by the object. This method is idempotent.
		'''
		if not self._disposed:
			self._dispose()
			self._disposed = True

	@abstractmethod
	def _dispose(self):
		'''
		Performs actual disposing, needs to be overridden by subclasses.
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
