#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import, print_function

import sys
import os
import thread

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer

from staticpycon import gen
from staticpycon import util


def serve():
    print("Listening on 127.0.0.1:8080 ...")
    server = TCPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
    os.chdir(gen.SITE_DIR)
    server.serve_forever()


def run(start_server=False, sass_only=False, debug=False):
    if not sass_only and start_server:
        thread.start_new_thread(serve, ())

    if sass_only:
        gen.render_scss(debug=debug)
    else:
        gen.gen(start_server=start_server, debug=debug)


if __name__ == "__main__":
    # 如果命令行参数含有-g则只生成网页，不启动自动生成服务
    # 如果含有 --sass 则只编译样式
    # 如果含有 -d 则不 minify CSS
    sass_only = '--sass' in sys.argv
    debug = '-d' in sys.argv
    start_server = not '-g' in sys.argv

    util.setup_logging()

    run(start_server=start_server, sass_only=sass_only, debug=debug)
