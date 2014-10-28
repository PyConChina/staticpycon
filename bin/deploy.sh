#!/bin/sh
# base incoming hooks API auto deploy new content from gitcafe
### changelog::
#   141022:ZQ creat base hook-deploy-by-git.sh
#=========================================================== var defines
VER="deploy.sh v14.10.22"
DATE=`date "+%y%m%d"`
#NOW=$(date +"%Y-%m-%d")
GIT="/usr/bin/git"
PY="/usr/bin/python"
#=========================================================== path defines
LOGF="/opt/logs/$DATE-cron-deploy.log"
RESPATH="/opt/www/staticpycon"
#=========================================================== action defines
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"  >> $LOGF
echo "###::$VER Hooks log 4 auto pull+gen from gitcafe"  >> $LOGF
echo "###::run@" `date +"%Y/%m/%d %H:%M:%S"` >> $LOGF
echo "<<<   trigging crontab tasks"  >> $LOGF

cd $RESPATH
#pwd            >> $LOGF 2>&1
$PY deploy.py   >> $LOGF 2>&1

echo "###::end@" `date +"%Y/%m/%d %H:%M:%S"` >> $LOGF
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"  >> $LOGF
#=========================================================== action DONE
#exit  0
