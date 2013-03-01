# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import abspath, dirname, join
from time import time

import sfml
from cg import ContextFactory
from cg.bridge import cgIsContext
from OpenGL import GL as gl

ROOT = abspath(dirname(__file__))

class App(object):
	def run(self):
		self.window = self.create_window()
		cg_context = self.create_cg_context()
		
		effect = cg_context.create_effect_from_file(join(ROOT, 'effect.cgfx'))
		self.technique = effect.techniques[0]

		self.running = True
		while self.running:
			self.process_events()

			self.window.clear(sfml.Color.BLACK)
			self.render()
			self.window.display()

		cg_context.dispose()
		self.window.close()

	def render(self):
		for pass_ in self.technique.passes:
			pass_.begin()

			gl.glClear(gl.GL_COLOR_BUFFER_BIT)
			gl.glLoadIdentity()

			gl.glBegin(gl.GL_TRIANGLES)
			gl.glVertex3f(-0.5, -0.5, 0)
			gl.glVertex3f(0.5, -0.5, 0)
			gl.glVertex3f(0, 0.5, 0)
			gl.glEnd()

			pass_.end()

	def create_window(self):
		window = sfml.RenderWindow(sfml.VideoMode(800, 600), 'python-cg example')
		window.vertical_sync_enabled = True
		return window

	def create_cg_context(self):
		cf = ContextFactory()
		return cf.create()

	def process_events(self):
		for event in self.window.iter_events():
			if event.type == sfml.Event.CLOSED:
				self.running = False


if __name__ == '__main__':
	app = App()
	app.run()
