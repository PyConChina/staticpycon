#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import

import os
import errno
import logging

from ._colorama_compat import colorama


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


def setup_logging():
    # scss compiler output
    logging.getLogger('scss.compiler').addHandler(SCSSMessagesHandler())


# formatter for pyScss messages
class SCSSMessagesFormatter(logging.Formatter):
    '''Formatter for pyScss outputs.'''

    FMT_WARNING = (
        colorama.Style.DIM
        + colorama.Fore.CYAN
        + 'scss '
        + colorama.Fore.YELLOW
        + 'warn '
        + colorama.Style.RESET_ALL
        + '%s'
    )

    def format(self, record):
        if record.levelno == logging.WARNING:
            return self.FMT_WARNING % (record.msg, )

        return super(SCSSMessagesFormatter, self).format(record)


class SCSSMessagesHandler(logging.StreamHandler):
    '''Logging handler for pyScss.'''

    def __init__(self, *args, **kwargs):
        super(SCSSMessagesHandler, self).__init__(*args, **kwargs)

        # use custom formatter
        self.setFormatter(SCSSMessagesFormatter())


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
