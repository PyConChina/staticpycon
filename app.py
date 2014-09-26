#!/usr/bin/env python
#encoding:utf8

from os.path import realpath, dirname, join, getmtime
from os import listdir
from staticjinja import make_renderer
from markdown import Markdown
import yaml, re

PROJECT_DIR = realpath(dirname(__file__))
SITE_DIR = join(PROJECT_DIR, "out")
SOURCE_DIR = join(PROJECT_DIR, "src")
ASSET_DIR = join(PROJECT_DIR, "src", "asset")
ASSET_DIR_REl = "asset"
DATA_DIR = join(PROJECT_DIR, "src", "data")

def mdconv(markdown_source):
    # md = Markdown(extensions=['meta', 'toc', 'tables', 'fenced_code'])
    md = Markdown()
    html_content = md.convert(markdown_source)
    return html_content

data_mtimes = {}
pycon_context = {
    'mdconv' : mdconv
}

def load_data():
    global data_mtimes
    global pycon_context
    for filename in listdir(DATA_DIR):
        filepath = join(DATA_DIR, filename)
        filemtime = int(getmtime(filepath))
        if filepath in data_mtimes and filemtime == data_mtimes[filepath]:
            continue # skip unmodified file
        data_mtimes[filepath] = filemtime
        if "_site.yaml" == filename:
            data = yaml.load(open(filepath))
            pycon_context.update(**data)
            continue
        entryname = re.search("_(\w+)\.yaml", filename).group(1)
        data = yaml.load(open(filepath))
        pycon_context[entryname] = data

def render_cn_page(renderer, template, **context):
    global pycon_context
    load_data()
    outfile = template.name.replace(".cn.html", ".html")
    filepath = join(SITE_DIR, outfile)
    template.stream(pycon_context).dump(filepath, "utf8")

def dev():
    renderer = make_renderer(searchpath=SOURCE_DIR, staticpath=ASSET_DIR_REl,
        outpath=SITE_DIR, rules=[
            ("\w+\.cn\.html", render_cn_page),
        ])
    def serve():
        from SimpleHTTPServer import SimpleHTTPRequestHandler
        from SocketServer import TCPServer
        import os
        print("Listening on 127.0.0.1:8080 ...")
        server = TCPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
        os.chdir(SITE_DIR)
        server.serve_forever()
    import thread
    thread.start_new_thread(serve, ())
    renderer.run(use_reloader=True)

if __name__ == "__main__":
    dev()