# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mock import Mock
from nose.tools import eq_, raises

from cg.utils import Disposable, gather

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

class TestGather(object):
	def test_gather_works_correctly(self):
		for data_set in (
			(),
			(1,),
			(3, 4, 5),
		):
			yield self.check_data_set, data_set

	def check_data_set(self, data_set):
		bridge = Mock()
		owner = 'xxx'

		def get_first(my_owner):
			eq_(my_owner, owner)
			return data_set[0] if data_set else None

		def get_next(element):
			index = data_set.index(element) + 1
			if index < len(data_set):
				return data_set[index]
			else:
				return None

		result = gather(owner, get_first, get_next)
		eq_(result, data_set)
