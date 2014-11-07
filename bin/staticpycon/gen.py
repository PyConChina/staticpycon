#!/usr/bin/env python
#encoding:utf8

from __future__ import unicode_literals, absolute_import, print_function
from os.path import realpath, dirname, join, getmtime, splitext, basename
from os.path import exists as file_exists
from os import listdir, makedirs, chdir
from staticjinja import make_renderer
import yaml, re, thread, sys
from copy import deepcopy
import glob

from ._vendor import scss

from .util import mkdirp

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
BOWER_DEP_DIR = join(PROJECT_DIR, "bower_components")
SITE_DIR = join(PROJECT_DIR, "out")
SOURCE_DIR = join(PROJECT_DIR, "src")
STYLESHEET_DIR = join(PROJECT_DIR, "sass")
ASSET_DIR = join(PROJECT_DIR, "src", "asset")
ASSET_DIR_REL = "asset"
DATA_DIR = join(PROJECT_DIR, "src", "data")
CSS_OUTPUT_DIR = join(SITE_DIR, ASSET_DIR_REL, "css")

SCSS_IMPORT_PATH = (
    STYLESHEET_DIR,
    join(BOWER_DEP_DIR, 'font-awesome/scss/'),
    join(BOWER_DEP_DIR, 'bourbon/dist/'),
    join(BOWER_DEP_DIR, 'neat/app/assets/stylesheets/'),
)

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

PROMPT_FMT_SCSS = (
    colorama.Style.DIM
    + colorama.Fore.CYAN
    + 'scss '
    + colorama.Fore.RESET
    + colorama.Style.RESET_ALL
    + '%s'
)

data_mtimes = {}
data_pattern = re.compile("_(\w+)\.yaml")
data_contexts = {
    'cn' : { 'lang' : 'cn', 'lang_suffix' : '_cn', 'lang_dir' : '' },
    'en' : { 'lang' : 'en', 'lang_suffix' : '_en', 'lang_dir' : 'en' },
}


def _sp_printlog(msg):
    '''模板函数，在生成日志中输出消息 '''
    print(msg)

def _sp_selectspeakers(speakers, city):
    '''模板函数，选择指定city的speakers'''
    keyname = "city_" + city
    return [ speaker for speaker_id, speaker in speakers.iteritems() \
        if keyname in speaker]

def process_data(data, suffix):
    '''数据处理函数，用于实现翻译文本的自动替换

    主要目的是把用suffix结尾的键对应的值覆盖无suffix结尾的键对应的值，
    如把name_en（_en是suffix）的值写到name中。处理过程中使用了递归。
    '''
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
    '''载入数据文件，保存了文件的mtime以减少不必要的读操作'''
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

def render_scss():
    # ensure output dir exists
    mkdirp(CSS_OUTPUT_DIR)

    for in_path in glob.iglob(join(STYLESHEET_DIR, '*.scss')):
        in_filename = basename(in_path)
        # don't process partials
        if in_filename.startswith('_'):
            continue

        out_filename = splitext(in_filename)[0] + '.css'
        out_path = join(CSS_OUTPUT_DIR, out_filename)
        print(PROMPT_FMT_SCSS % (out_path, ))

        with open(in_path, 'rb') as fp:
            content = fp.read()

        result = scss.compiler.compile_string(
            content,
            search_path=SCSS_IMPORT_PATH,
            output_style='compressed',  # TODO: use expanded while debugging?
        )

        with open(out_path, 'wb') as fp:
            fp.write(result.encode('utf-8'))

def gen(start_server=False):
    # Sass
    render_scss()

    # Pages
    for lang, context in data_contexts.iteritems():
        context['printlog'] = _sp_printlog
        context['selectspeakers'] = _sp_selectspeakers
    renderer = make_renderer(searchpath=SOURCE_DIR, staticpath=ASSET_DIR_REL,
        outpath=SITE_DIR, rules=[
            ("[\w-]+\.html", render_page)
        ])

    renderer.run(use_reloader=start_server)

if __name__ == "__main__":
    colorama.init()
    gen(start_server=(not "-g" in sys.argv))
