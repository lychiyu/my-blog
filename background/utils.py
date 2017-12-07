# -*-coding: utf-8 -*-
import qiniu, hashlib, time
from django.conf import settings

q = qiniu.Auth(settings.QINIU['access_key'], settings.QINIU['secret_key'])


def qiniu_upload(data, prefix='', mime_type='application/octet-stream', key=None):
    prefix = prefix if not prefix.startswith('/') else prefix[1:]
    prefix = prefix if prefix.endswith('/') or prefix == '' else prefix + '/'
    if key == None:
        key = '%s%d_%s' % (prefix, int(time.time()), hashlib.md5(data).hexdigest())
    token = q.upload_token(settings.QINIU['bucket_name'], key, 3600)
    ret, info = qiniu.put_data(token, key, data, mime_type=mime_type)
    return ret, info
