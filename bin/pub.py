#!/usr/bin/env python
#encoding:utf-8

from sys import stderr
import app
import qiniu.conf, qiniu.rs, qiniu.rsf, qiniu.io

def print_error(msg):
    stderr.write("[ERROR] %s\n" % msg)

try:
    from pubconf import *
except ImportError:
    print_error("pubconf.py not existed.")
    exit(-1)

def _setup():
    qiniu.conf.ACCESS_KEY = PUB_ACCESS_KEY
    qiniu.conf.SECRET_KEY = PUB_SECRET_KEY

def _generate_site():
    print("Generating the new site in %s ..." % app.SITE_DIR)
    app.run(start_server=False)

def _list_site(bucket=PUB_BUCKET, prefix=PUB_SITE_PREFIX):
    rs, marker, err, files = qiniu.rsf.Client(), None, None, []
    while err is None:
        ret, err = rs.list_prefix(bucket, prefix=prefix, marker=marker)
        if ret is None:
            continue
        marker = ret.get('marker', None)
        files.extend([ item['key'] for item in ret['items'] ])
        # print("\n".join(files))
    if err is not qiniu.rsf.EOF:
        print_error("%s" % err)
    return files

def _upload_site(site_dir):
    print("Uploading the new site ...")
    files_ready = []
    import os, os.path
    from os.path import join
    for root, dirs, files in os.walk(site_dir):
        if not files: continue
        files_ready.extend([join(root, f) for f in files])
    uptoken = qiniu.rs.PutPolicy(PUB_BUCKET).token()
    for f in files_ready:
        print("Uploading %s ..." % (f,))
        key = join(PUB_SITE_PREFIX, f.replace(site_dir, "").lstrip("/"))
        qiniu.rs.Client().delete(PUB_BUCKET, key) # try deleting
        ret, err = qiniu.io.put_file(uptoken, key, f)
        if err is not None:
            print_error("Failed to upload %s as %s" % (f, err))

def main():
    # setup
    _setup()
    # generate sites
    _generate_site()
    # publish sites
    _upload_site(app.SITE_DIR)
    print("Done!")

if __name__ == "__main__":
    main()
