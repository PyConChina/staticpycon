#!/usr/bin/env python
#encoding:utf8

from os.path import realpath, dirname, join, getmtime
from os.path import exists as file_exists
from os import listdir, makedirs, chdir
from staticjinja import make_renderer
import yaml, re, thread, sys
from copy import deepcopy

PROJECT_DIR = realpath(dirname(__file__))
SITE_DIR = join(PROJECT_DIR, "out")
SOURCE_DIR = join(PROJECT_DIR, "src")
ASSET_DIR = join(PROJECT_DIR, "src", "asset")
ASSET_DIR_REL = "asset"
DATA_DIR = join(PROJECT_DIR, "src", "data")

data_mtimes = {}
data_pattern = re.compile("_(\w+)\.yaml")
data_contexts = {
    'cn' : { 'lang' : 'cn', 'lang_suffix' : '_cn', 'lang_dir' : '' },
    'en' : { 'lang' : 'en', 'lang_suffix' : '_en', 'lang_dir' : 'en' },
}

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
                    print('Warning: invalid attribute %s' % kn)

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
            for lang, context in data_contexts.items():
                data_copy = deepcopy(data)
                process_data(data_copy, context['lang_suffix'])
                context[entryname] = data_copy

def render_page(renderer, template, **context):
    load_data()
    for lang, context in data_contexts.items():
        outfile = join(SITE_DIR, context['lang_dir'], template.name)
        head = dirname(outfile)
        if head and not file_exists(head):
            makedirs(head)
        print("Generating [%s] %s ... " % (context['lang'], outfile))
        template.stream(context).dump(outfile, "utf-8")

def main():
    renderer = make_renderer(searchpath=SOURCE_DIR, staticpath=ASSET_DIR_REL,
        outpath=SITE_DIR, rules=[
            ("[\w-]+\.html", render_page)
        ])
    def serve():
        from SimpleHTTPServer import SimpleHTTPRequestHandler
        from SocketServer import TCPServer
        print("Listening on 127.0.0.1:8080 ...")
        server = TCPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
        chdir(SITE_DIR)
        server.serve_forever()
    dev_mode = (not "-g" in sys.argv)
    if dev_mode: thread.start_new_thread(serve, ())
    renderer.run(use_reloader=dev_mode)

if __name__ == "__main__":
    main()
