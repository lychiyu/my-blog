# -*- coding: utf-8 -*-
from .models import UserInfo


def require_login(func):
    def wrapper(request, *args, **kargs):
        user_id = request.session.get('user')
        if not user_id:
            return {'code': -1, 'msg': u'请先登录'}
        request.user = UserInfo.objects.filter(id=user_id, status=1).first()
        if not request.user:
            return {'code': -1, 'msg': u'请先登录'}
        return func(request, *args, **kargs)

    return wrapper


def require_admin(func):
    @require_login
    def wrapper(request, *args, **kargs):
        if request.user.type != 1:
            return {'code': -1, 'msg': u'权限不足'}
        return func(request, *args, **kargs)

    return wrapper
