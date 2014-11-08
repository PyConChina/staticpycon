#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import, print_function

import time


def gen_cachebuster_qs():
    '''生成可直接附着在静态资源 URL 之后的 cachebuster query string.

    内容即为构建开始时间的 Unix 时间戳.

    '''

    return '?_t={}'.format(int(time.time()))


# vim:set ai et ts=4 sts=4 fenc=utf-8:
