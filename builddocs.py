# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

from os.path import dirname, join
from subprocess import check_call

def main():
	check_call([sys.executable, 'setup.py', 'build_ext', '--inplace'])
	sphinx_build = join(dirname(sys.executable), 'sphinx-build')
	check_call([sphinx_build, '-b', 'html', 'docs', join('docs', '_build', 'html')])

if __name__ == '__main__':
	main()
