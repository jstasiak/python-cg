# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg.effect.pass_ import Pass
from cg.utils import gather, ReprMixin

class EffectTechnique(ReprMixin):
	'''
	Effect technique.
	'''

	repr_members = ('name', 'valid',)

	_passes = None

	def __init__(self, cgtechnique, bridge, name, valid):
		self._cgtechnique = cgtechnique
		self._bridge = bridge

		#: Gets the name of the technique (string)
		self.name = name

		#: Gets whether the technique is valid on current hardware or not (bool)
		self.valid = valid

	@property
	def passes(self):
		'''
		Gets technique passes as a tuple of :py:class:`cg.effect.pass_.Pass`
		'''
		if self._passes is None:
			self._passes = tuple(Pass(cg_pass, self._bridge) for cg_pass in gather(
				self._cgtechnique, self._bridge.cgGetFirstPass, self._bridge.cgGetNextPass))

		return self._passes

class EffectTechniqueCollection(tuple):
	@property
	def by_name(self):
		'''
		Gets technique dictionary indexed by names.
		'''
		return dict((t.name, t) for t in self)

class EffectTechniqueFactory(object):
	def __init__(self, bridge):
		self._bridge = bridge

	def get_by_cgtechnique(self, cgtechnique):
		name = self._bridge.cgGetTechniqueName(cgtechnique)
		valid = self._bridge.cgValidateTechnique(cgtechnique)

		return EffectTechnique(
			bridge=self._bridge,
			cgtechnique=cgtechnique,
			name=name,
			valid=valid
		)

	def get_by_cgeffect(self, cgeffect):
		cgtechniques = gather(
			cgeffect,
			self._bridge.cgGetFirstTechnique, self._bridge.cgGetNextTechnique
		)
		return EffectTechniqueCollection(self.get_by_cgtechnique(cgt) for cgt in cgtechniques)
