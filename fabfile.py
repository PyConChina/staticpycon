from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
#########################################
#   deploy for 7niu CDN
#########################################
#env.input_path = 'docs'
env.deploy_path = 'out'
DEPLOY_PATH = env.deploy_path

env.qiniu = '/opt/bin/7niu_package_darwin_amd64/qrsync'
env.qiniu_conf = '../7niu-pycon.json'
env.qiniu_path = '../7niu.pyconcn'

local_settings = os.path.expanduser(
    os.path.join(os.path.dirname(__file__), 'local_settings.py'))
if os.path.exists(local_settings):
    execfile(local_settings)

def put7niu():
    local('cd {qiniu_path} && '
            'pwd && '
            'python gen4idx.py ./ footer-7niu.html 201 && '
            '{qiniu} -skipsym {qiniu_conf}&& '
            'pwd '.format(**env)
          )

#   141013 ZQ appended new actions for pub. through gitcafe-pages
'''depend on:
0. ACL for https://gitcafe.com/PyConChina/PyConChina
1. re-link staticpycon/out -> ../7niu.pyconcn/2014/
2. editor ../7niu.pyconcn/2014/.git/config appended like
...

[branch "gitcafe-pages"]
    remote = cafe
    merge = refs/heads/gitcafe-pages
...

confirmed all OK this flow:

- fixed some src/data/*.md 
- python bin/app.py -g
- cd out
- git ci -am "commit log some"
- git pu

so the daily working just:

    $ fab pub2cafe

'''
#########################################
#   deploy for gitcafe-pages
#########################################
def build():
    local('python bin/app.py -g')

def pub2cafe():
    build()
    local('cd {deploy_path} && '
            'git status && '
            'git add . && '
            'git commit -am \'upgraded from local. by StaticPyCon\' && '
            'git push origin gitcafe-pages'.format(**env)
          )

# Remote server configuration
#   deploy for upstream pycon-statics hosts
#env.roledefs = {
#        'smirrors': ['obp:9022'
#            , 'root@PyConSS1'
#            , 'root@PyConSS3'
#            ]
#    }
#env.out_dir = '/opt/www/PyConChina/'
#
#@roles('smirrors')
#def sync2upstreams():
#    with cd('{out_dir}'.format(**env)):
#        run('uname -a')
#        run('pwd')
#        run("git status" )
#        run("git pull" )
#########################################
#   deploy for upstream pycon-statics hosts
#########################################
#env.roledefs = {
#        'smirror': ['gw2obp']
#    }
env.static_site = '/opt/www/staticpycon'

#@roles('smirror')
#def sync4upstream():
#    local('ssh gw2obp uname -a ; '
#            'cat {static_site}/deploy.py ; '
#            'cd {static_site} ; '
#            'python {static_site}/deploy.py'.format(**env)
#        )


