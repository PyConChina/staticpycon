#!/bin/sh
#
#########################################
#   deploy for upstream pycon-statics hosts
#########################################
#=========================================================== var defines
# Change following ines
PATH="/opt/www/staticpycon"
DEPLOY="python ./deploy.py"
#=========================================================== path defines
#=========================================================== action defines
cd $PATH

pwd

$DEPLOY  #>/dev/null 2>&1

#=========================================================== action DONE
#exit  0
