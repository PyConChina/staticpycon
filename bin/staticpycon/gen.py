#!/usr/bin/env python
#encoding:utf8

from os.path import realpath, dirname, join, getmtime
from os.path import exists as file_exists
from os import listdir, makedirs, chdir
from staticjinja import make_renderer
import yaml, re, thread, sys
from copy import deepcopy

try:
    import colorama
except ImportError:
    # just stub out ANSI control codes
    class colorama(object):
        class Style(object):
            DIM = RESET_ALL = ''

        class Fore(object):
            BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
            RESET = ''

        @staticmethod
        def init():
            pass


PROJECT_DIR = dirname(dirname(realpath(dirname(__file__))))
SITE_DIR = join(PROJECT_DIR, "out")
SOURCE_DIR = join(PROJECT_DIR, "src")
ASSET_DIR = join(PROJECT_DIR, "src", "asset")
ASSET_DIR_REL = "asset"
DATA_DIR = join(PROJECT_DIR, "src", "data")

PROMPT_FMT_HTML = (
    colorama.Style.DIM
    + colorama.Fore.CYAN
    + 'html '
    + colorama.Fore.GREEN
    + '[%s] '
    + colorama.Fore.RESET
    + colorama.Style.RESET_ALL
    + '%s'
)

PROMPT_FMT_INVALID_ATTR = (
    colorama.Style.DIM
    + colorama.Fore.YELLOW
    + 'warn '
    + colorama.Style.RESET_ALL
    + colorama.Fore.MAGENTA
    + 'invalid attribute '
    + colorama.Fore.RESET
    + '%s'
)

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
                    print(PROMPT_FMT_INVALID_ATTR % (kn, ))

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
        print(PROMPT_FMT_HTML % (context['lang'], outfile))
        template.stream(context).dump(outfile, "utf-8")

def gen(start_server=False):
    renderer = make_renderer(searchpath=SOURCE_DIR, staticpath=ASSET_DIR_REL,
        outpath=SITE_DIR, rules=[
            ("[\w-]+\.html", render_page)
        ])
    return renderer.run(use_reloader=start_server)


if __name__ == "__main__":
    colorama.init()
    gen(start_server=(not "-g" in sys.argv))
