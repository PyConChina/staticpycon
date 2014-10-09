#!/usr/bin/env python
#encoding:utf8

from os.path import realpath, dirname, join, getmtime
from os.path import exists as file_exists
from os import listdir, makedirs
from staticjinja import make_renderer
import yaml, re
from copy import deepcopy

PROJECT_DIR = realpath(dirname(__file__))
SITE_DIR = join(PROJECT_DIR, "out")
SOURCE_DIR = join(PROJECT_DIR, "src")
ASSET_DIR = join(PROJECT_DIR, "src", "asset")
ASSET_DIR_REl = "asset"
DATA_DIR = join(PROJECT_DIR, "src", "data")

data_mtimes = {}
data_table = {
    'cn' : {
        'suffix'  : '_cn',
        'basedir' : "",
        'context' : { 'lang' : 'cn' }
    },
    'en' : {
        'suffix'  : '_en',
        'basedir' : 'en',
        'context' : { 'lang' : 'en' }
    }
}
data_pattern = re.compile("_(\w+)\.yaml")

def process_data(data, suffix):
    if isinstance(data, list):
        for v in data:
            process_data(v, suffix)
    elif isinstance(data, dict):
        for k, v in data.iteritems():
            if isinstance(v, list) or isinstance(v, dict):
                process_data(v, suffix)
            if k.endswith(suffix):
                kn = k[:-len(suffix)]
                if kn in data:
                    data[kn] = v
                else:
                    print 'Warning: invalid attribute ', kn

def load_data():
    for filename in listdir(DATA_DIR):
        filepath = join(DATA_DIR, filename)
        filemtime = int(getmtime(filepath))
        if filepath in data_mtimes and filemtime == data_mtimes[filepath]:
            continue # skip unmodified file
        match = data_pattern.match(filename)
        if match:
            data_mtimes[filepath] = filemtime
            entryname = match.group(1)
            data = yaml.load(open(filepath))
            for lang, v in data_table.iteritems():
                data_copy = deepcopy(data)
                process_data(data_copy, v['suffix'])
                v['context'][entryname] = data_copy

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
