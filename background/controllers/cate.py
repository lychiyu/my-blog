# -*- coding: utf-8 -*-

from ..models import CateInfo
from ..auth import require_login


@require_login
def add_cate(request):
    name = request.POST.get('name')
    if not name:
        return {'code': 1, 'msg': '请输入类型名'}
    cate = CateInfo.objects.filter(name=name, status=1).first()
    if cate:
        return {'code': 1, 'msg': '该类型名已经存在'}
    cate = CateInfo.objects.create(name=name, status=1)
    cate.name = name
    cate.save()
    return {'code': 0}


@require_login
def delete_cate(request):
    id = request.POST.get('id')
    if not id:
        return {'code': 1, 'msg': '请给出类型id'}
    cate = CateInfo.objects.filter(id=id, status=1).first()
    if not cate:
        return {'code': 1, 'msg': '该类型不存在'}
    cate.status = 0
    cate.save()
    return {'code': 0}


@require_login
def modify_cate(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if not id:
        return {'code': 1, 'msg': '请给出类型id'}

    cate = CateInfo.objects.filter(name=name).exclude(id=id).first()
    if cate:
        return {'code': 1, 'msg': '该类型名已被占用'}

    cate = CateInfo.objects.filter(id=id).first()
    if not cate:
        return {'code': 1, 'msg': '该类型不存在'}
    cate.name = name
    cate.status = status
    cate.save()
    return {'code': 0}


def get_cate(request):
    id = request.GET.get('id')
    if not id:
        return {'code': 1, 'msg': '请给出类型id'}
    cate = CateInfo.objects.filter(id=id).first()
    if not cate:
        return {'code': 1, 'msg': '该类型不存在'}
    data = ({'id': cate.id, 'name': cate.name, 'status': cate.status})
    return {'code': 0, 'data': data}


def get_cate_list(request):
    cate_list = CateInfo.objects.filter(status=1)
    if request.session['user']:
        cate_list = CateInfo.objects.filter()

    data = []
    for cate in cate_list:
        data.append({'id': cate.id, 'name': cate.name, 'status': cate.status})

    return {'code': 0, 'data': data}
