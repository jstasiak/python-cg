# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

from pkg_resources import load_entry_point
from subprocess import check_call

def main():
	check_call([sys.executable, 'setup.py', 'build_ext', '--inplace'])
	sys.exit(
		load_entry_point('nose', 'console_scripts', 'nosetests')()
	)

if __name__ == '__main__':
	main()
