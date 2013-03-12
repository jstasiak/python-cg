# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mock import Mock
from nose.tools import eq_

from cg.context import Context, ContextFactory

class TestContextFactory(object):
	def test_context_gets_created_correctly(self):
		handle = 123
		bridge = Mock()
		bridge.cgCreateContext.return_value = handle

		cf = ContextFactory(bridge)
		context = cf.create()
		eq_(context._cgcontext, handle)

class TestContext(object):
	def test_context_disposes_of_its_resources(self):
		handle = 234
		bridge = Mock()

		context = Context(handle, bridge)
		context.dispose()

		bridge.cgDestroyContext.assert_called_once_with(handle)
