#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import, print_function

import sys
import os
import thread

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer

from staticpycon import gen


def serve():
    print("Listening on 127.0.0.1:8080 ...")
    server = TCPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
    os.chdir(gen.SITE_DIR)
    server.serve_forever()


def run(start_server=False):
    if start_server:
        thread.start_new_thread(serve, ())

    gen.gen(start_server=start_server)


if __name__ == "__main__":
    run(start_server=(not "-g" in sys.argv))
