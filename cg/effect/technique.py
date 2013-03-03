# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.effect.pass_ import Pass
from cg.utils import gather

class Technique(object):
	'''
	Effect technique.
	'''

	_passes = None

	def __init__(self, cgtechnique, bridge):
		self._cgtechnique = cgtechnique
		self._bridge = bridge

	@property
	def passes(self):
		'''
		Gets technique passes as a tuple of :py:class:`cg.effect.pass_.Pass`
		'''
		if self._passes is None:
			self._passes = tuple(Pass(cg_pass, self._bridge) for cg_pass in gather(
				self._cgtechnique, self._bridge.cgGetFirstPass, self._bridge.cgGetNextPass))

		return self._passes
