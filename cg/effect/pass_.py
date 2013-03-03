# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class Pass(object):
	'''
	Contains state for rendering with an effect.
	'''

	def __init__(self, cgpass, bridge):
		self._cgpass = cgpass
		self._bridge = bridge

	def begin(self):
		'''
		Begins the rendering pass.

		.. seealso::
		
			Function `cgSetPassState <http://http.developer.nvidia.com/Cg/cgSetPassState.html>`_
				This function is used internally by :py:meth:`begin`.
		'''
		self._bridge.cgSetPassState(self._cgpass)
	
	def end(self):
		'''
		Ends the rendering pass.

		.. seealso::
		
			Function `cgResetPassState <http://http.developer.nvidia.com/Cg/cgResetPassState.html>`_
				This function is used internally by :py:meth:`end`.
		'''
		self._bridge.cgResetPassState(self._cgpass)
