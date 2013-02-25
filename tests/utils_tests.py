# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import eq_, raises

from cg.utils import Disposable

class TestDisposable(object):
	def setup(self):
		class TestClass(Disposable):
			counter = 0

			def _dispose(self):
				self.counter += 1

		self.TestClass = TestClass

	@raises(TypeError)
	def test_disposable_is_actually_abstract(self):
		disposable = Disposable()

	
	def test_dispose_is_idempotent(self):
		disposable = self.TestClass()
		counters = [disposable.counter]

		dispose_count = 3
		for i in range(dispose_count):
			disposable.dispose()
			counters.append(disposable.counter)

		eq_(counters, [0] + [1] * dispose_count)
	
	def test_dispose_is_called_from_finalizer(self):
		disposable = self.TestClass()
		disposable.__del__()
		eq_(disposable.counter, 1)
