# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mock import Mock

from cg.effect import Effect

class TestEffect(object):
	def test_effect_disposes_of_resources_properly(self):
		cgeffect = 99
		bridge = Mock()

		effect = Effect(cgeffect, bridge)
		effect.dispose()

		bridge.cgDestroyEffect.assert_called_once_with(cgeffect)
