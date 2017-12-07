# -*- coding: utf-8 -*-

import hashlib
from ..auth import require_login
from ..models import UserInfo
from django.conf import settings


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(request.POST)
    print(username, password)
    if not username or not password:
        return {'code': 1, 'msg': '请输入用户名和密码'}
    user = UserInfo.objects.filter(username=username, password=hashlib.md5((password+settings.SECRET_KEY).encode('utf-8')).hexdigest(), status=1).first()
    if not user:
        return {'code': 1, 'msg': '用户不存在或密码错误'}

    request.session['user'] = user.id
    data = ({'id': user.id, 'username': user.username, 'type': user.type})
    return {'code': 0, 'data': data}


@require_login
def logout(request):
    del request.session['user']
    return {'code': 0}


def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return {'code': 1, 'msg': '请输入用户名和密码'}
    user = UserInfo.objects.filter(username=username).first()
    if user:
        return {'code': 1, 'msg': '该用户名已经被占用'}
    user = UserInfo.objects.create(username=username, password=hashlib.md5((password+settings.SECRET_KEY).encode('utf-8')).hexdigest())
    user.save()
    return {'code': 0}
