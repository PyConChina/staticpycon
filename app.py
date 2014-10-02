#!/usr/bin/env python
#encoding:utf8

from os.path import realpath, dirname, join, getmtime
from os.path import exists as file_exists
from os import listdir, makedirs
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
    md = Markdown()
    html_content = md.convert(markdown_source)
    return html_content

data_mtimes = {}
data_table = {
    'cn' : {
        'basedir' : "",
        'pattern' : re.compile("_(\w+)\.cn\.yaml"),
        'context' : { 'mdconv' : mdconv, 'lang' : 'cn' }
    },
    'en' : {
        'basedir' : 'en',
        'pattern' : re.compile("_(\w+)\.en\.yaml"),
        'context' : { 'mdconv' : mdconv, 'lang' : 'en' }
    }
}

def load_data():
    for filename in listdir(DATA_DIR):
        filepath = join(DATA_DIR, filename)
        filemtime = int(getmtime(filepath))
        if filepath in data_mtimes and filemtime == data_mtimes[filepath]:
            continue # skip unmodified file
        for lang, v in data_table.iteritems():
            match = v['pattern'].match(filename)
            if match:
                data_mtimes[filepath] = filemtime
                entryname = match.group(1)
                data = yaml.load(open(filepath))
                v['context'][entryname] = data
                break

def render_page(renderer, template, **context):
    load_data()
    for lang, v in data_table.iteritems():
        outfile = join(SITE_DIR, v['basedir'], template.name)
        # ensure dir
        head = dirname(outfile)
        if head and not file_exists(head):
            makedirs(head)
        print "Generating [%s] %s ..." % (lang, outfile)
        template.stream(v['context']).dump(outfile, "utf8") 

def dev():
    renderer = make_renderer(searchpath=SOURCE_DIR, staticpath=ASSET_DIR_REl,
        outpath=SITE_DIR, rules=[
            ("[\w-]+\.html", render_page)
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