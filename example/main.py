# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import abspath, dirname, join
from math import pi, sin, tan
from time import clock

import Image
import sfml

from numpy import array, float32, uint8
from OpenGL import GL as gl
from pyrr import matrix44

from cg import Cg

ROOT = abspath(dirname(__file__))

class App(object):
	def run(self):
		self.window = self.create_window()
		context = self.create_cg_context()
		context.register_states()
		context.manage_texture_parameters = True
		
		effect = context.create_effect_from_file(join(ROOT, 'effect.cgfx'))

		self.load_texture(join(ROOT, 'texture.png'),
			effect.parameters.by_name['texture'])
		self.time_parameter = effect.parameters.by_name['time']
		self.model_view_proj = effect.parameters.by_name['modelViewProj']

		valid_techniques = [t for t in effect.techniques if t.valid]
		assert valid_techniques
		self.technique = valid_techniques[0]

		print('techniques:')
		import pprint; pprint.pprint(effect.techniques.by_name)
		print('parameters:')
		import pprint; pprint.pprint(effect.parameters.by_name)

		self.running = True
		while self.running:
			self.process_events()

			self.window.clear(sfml.Color.BLACK)
			self.render()
			self.window.display()

		context.dispose()
		self.cg.dispose()
		self.window.close()

	def load_texture(self, filename, parameter):
		image = Image.open(filename)

		data = image.tostring('raw', 'RGB', 0, -1)

		gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

		to = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, to)
		parameter.set_value(to)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB,
			image.size[0], image.size[1], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, data)

	def render(self):
		t = clock()
		self.time_parameter.set_value(t)

		data = (
			((-0.5, -0.5, 0), (0.0, 0.0)),
			((0.5, -0.5, 0), (1.0, 0.0)),
			((0, 0.5, 0), (0.5, 1.0)),
		)

		proj = matrix44.create_perspective_projection_matrix(
			90, 4.0 / 3.0, 0.01, 100.0)

		mv = matrix44.multiply(
			matrix44.create_from_translation((sin(t * 10), 0.0, -3.0 * abs(sin(t * 30)))),
			matrix44.create_from_z_rotation(t * 50),
		)
 
		mvp = matrix44.multiply(mv, proj)

		self.model_view_proj.set_value(mvp)

		for pass_ in self.technique.passes:
			pass_.begin()

			gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

			gl.glBegin(gl.GL_TRIANGLES)

			for position, texcoord in data:
				gl.glMultiTexCoord2fv(gl.GL_TEXTURE0, texcoord)
				gl.glVertex3fv(position)

			gl.glEnd()

			pass_.end()

	def create_window(self):
		window = sfml.RenderWindow(sfml.VideoMode(800, 600), 'python-cg example')
		window.vertical_sync_enabled = True
		return window

	def create_cg_context(self):
		self.cg = Cg()
		return self.cg.create_context()

	def process_events(self):
		for event in self.window.iter_events():
			if event.type == sfml.Event.CLOSED:
				self.running = False


if __name__ == '__main__':
	app = App()
	app.run()
