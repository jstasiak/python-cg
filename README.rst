python-cg
=========

.. image:: https://travis-ci.org/jstasiak/python-cg.png?branch=master
   :alt: Build status
   :target: https://travis-ci.org/jstasiak/python-cg

What is it?
-----------

*python-cg* is a Python wrapper for `NVidia Cg Toolkit <https://developer.nvidia.com/cg-toolkit>`_ runtime.

Why create this project?
------------------------

* I like Cg
* I like Python
* I'm interested in computer games and 3D graphics
* It's fun

Requirements
------------

This project requires:

* NVidia Cg Toolkit ≥ 3.0
* Python 2.x ≥ 2.6, 3.x ≥ 3.2 or PyPy 1.9+ + development files
* C and C++ compilers

Python packages required to build and install *python-cg*:

* Cython ≥ 0.18
* numpy

To build documentation/run tests you also need:

* Mock ≥ 1.0
* Nose ≥ 1.2
* Sphinx ~ 1.2 (development version)

Building
--------

To build the project in place, run::

   python setup.py build_ext --inplace

Testing
-------

To run tests, execute::

   python runtests.py

Building the documentation
--------------------------

To build the documentation, call::

   python builddocs.py

Generated HTML files are placed in ``gh-pages/html`` directory.

Example usage
-------------

You can find example application using *python-cg* in ``example`` directory. Please note that
it requires (in addition to *python-cg* requirements):

* Development version of SFML 2
* Python packages listed in ``example/requirements.txt``::

   pip install -r example/requirements.txt

Then to run the example::

   python setup.py build_ext --inplace
   PYTHONPATH=. python example/main.py

License
-------

© 2013, Jakub Stasiak

This project is licensed under BSD License, see `LICENSE <LICENSE>`_ file for details.
