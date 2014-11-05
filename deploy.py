#!/usr/bin/env python
import os
import sys
'''deploy support
- 141028 upgrade usage 'app.py -g'
- 141010 usage 'gen.py'
'''

pipe = os.popen("git pull origin master").read()

if 'up-to-date' in pipe:
    sys.exit(1)
else:
    os.system("python ./bin/app.py -g ")
