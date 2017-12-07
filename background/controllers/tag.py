# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from ..models import TagInfo
from ..auth import require_login


@require_login
def add_tag(request):
    name = request.POST.get('name')
    if not name:
        return {'code': 1, 'msg': '请输入标签名'}
    tag = TagInfo.objects.filter(name=name, status=1).first()
    if tag:
        return {'code': 1, 'msg': '该标签名已经存在'}
    tag = TagInfo.objects.create(name=name, status=1)
    tag.name = name
    tag.save()
    return {'code': 0}


@require_login
def delete_tag(request):
    id = request.POST.get('id')
    if not id:
        return {'code': 1, 'msg': '请给出标签id'}
    tag = TagInfo.objects.filter(id=id, status=1).first()
    if not tag:
        return {'code': 1, 'msg': '该标签不存在'}
    tag.status = 0
    tag.save()
    return {'code': 0}


@require_login
def modify_tag(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if not id:
        return {'code': 1, 'msg': '请给出标签id'}

    tag = TagInfo.objects.filter(name=name).exclude(id=id).first()
    if tag:
        return {'code': 1, 'msg': '该标签名已被占用'}

    tag = TagInfo.objects.filter(id=id).first()
    if not tag:
        return {'code': 1, 'msg': '该标签不存在'}
    tag.name = name
    tag.status = status
    tag.save()
    return {'code': 0}


def get_tag(request):
    id = request.GET.get('id')
    if not id:
        return {'code': 1, 'msg': '请给出标签id'}
    tag = TagInfo.objects.filter(id=id).first()
    if not tag:
        return {'code': 1, 'msg': '该标签不存在'}
    data = ({'id': tag.id, 'name': tag.name, 'status': tag.status})
    return {'code': 0, 'data': data}


def get_tag_list(request):
    tag_list = TagInfo.objects.filter(status=1)
    if request.session.get('user'):
        tag_list = TagInfo.objects.all()

    data = []
    for tag in tag_list:
        data.append(
            {'id': tag.id, 'name': tag.name, 'amount': tag.postinfo_set.filter(status=1).count(), 'status': tag.status})

    return {'code': 0, 'data': data}
