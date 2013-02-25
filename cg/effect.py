# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.utils import Disposable
from cg.technique import Technique

class Effect(Disposable):
	_techniques = None

	def __init__(self, cgeffect, bridge):
		self._cgeffect = cgeffect
		self._bridge = bridge

	@property
	def techniques(self):
		if self._techniques is None:
			techniques = []
			technique = self._bridge.cgGetFirstTechnique(self._cgeffect)
			while technique:
				techniques.append(Technique(technique, self._bridge))
				technique = self._bridge.cgGetNextTechnique(technique)
			self._techniques = tuple(techniques)

		return self._techniques

	def _dispose(self):
		self._bridge.cgDestroyEffect(self._cgeffect)
