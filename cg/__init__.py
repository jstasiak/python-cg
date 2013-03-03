# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cg import bridge
from cg.context import ContextFactory
from cg.utils import Disposable

class CG(Disposable):
    '''
    Gateway to using python-cg.
    
    .. note:: This is the only class that should (or need to) be manually instantiated
    by user code.

    .. note:: There should be one instance of this class per process. Having multiple
        instances, although possible, can result in some unexpected behaviour.
    '''
    def __init__(self, context_factory=None):
        self._context_factory = context_factory or ContextFactory(bridge)

    def create_context(self):
        '''
        Creates CG context.

        :rtype: :py:class:`cg.context.Context`
        '''
        return self._context_factory.create()

    def perform_dispose(self):
        pass
