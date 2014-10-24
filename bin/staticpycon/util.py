#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import

import os
import errno


# http://stackoverflow.com/a/600612/596531
def mkdirp(path):
    '''``mkdir -p`` for Python.'''

    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
