#!/bin/sh
#
#########################################
#   deploy for upstream pycon-statics hosts
#########################################
#=========================================================== var defines
# Change following ines
PATH="/opt/www/staticpycon"
PY="/usr/bin/python"  #$(which python)
GIT="/usr/bin/git"    #$(which git)
DEPLOY="$PY ./deploy.py"
#=========================================================== path defines
#=========================================================== action defines
cd $PATH

pwd

$GIT pull origin master

$DEPLOY  #>/dev/null 2>&1

#=========================================================== action DONE
#exit  0
