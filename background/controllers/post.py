# -*- coding: utf-8 -*-
import datetime
from ..models import UserInfo, TagInfo, CateInfo, PostInfo
from ..auth import require_login
from ..utils import qiniu_upload
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@require_login
def add_post(request):
    title = request.POST.get('title')
    abstract = request.POST.get('abstract')
    logo = request.POST.get('logo')
    md_content = request.POST.get('md_content')
    html_content = request.POST.get('html_content')
    cate_id = request.POST.get('cate_id')
    tags = request.POST.get('tags')
    author = request.user
    if not title or not abstract or not md_content or not html_content or not cate_id or not tags:
        return {'code': 1, 'msg': '请求参数不完整'}
    cate = CateInfo.objects.filter(id=cate_id, status=1).first()
    if not cate:
        return {'code': 1, 'msg': '你选择的类型不存在'}
    tags = tags.split(',')
    if len(tags) == 0:
        return {'code': 1, 'msg': '请为文章选择所属的标签'}
    params = {'title': title, 'abstract': abstract, 'md_content': md_content, 'html_content': html_content,
              'cate': cate, 'author': author, 'logo': logo}
    post = PostInfo.objects.create(**params)
    for tag_id in tags:
        tag = TagInfo.objects.filter(id=tag_id, status=1).first()
        if tag:
            post.tags.add(tag)
    post.save()
    return {'code': 0}


@require_login
def delete_post(request):
    id = request.POST.get('id')
    if not id:
        return {'code': 1, 'msg': '请传入要删除文章的id'}
    post = PostInfo.objects.filter(author=request.user, status=1, id=id).first()
    if not post:
        return {'code': 1, 'msg': '文章不存在'}
    post.status = 0
    post.save()
    return {'code': 0}


@require_login
def modify_post(request):
    id = request.POST.get('id')
    if not id:
        return {'code': 1, 'msg': '请传入要删除文章的id'}
    post = PostInfo.objects.filter(author=request.user, id=id).first()
    if not post:
        return {'code': 1, 'msg': '文章不存在'}

    title = request.POST.get('title')
    abstract = request.POST.get('abstract')
    logo = request.POST.get('logo')
    md_content = request.POST.get('md_content')
    html_content = request.POST.get('html_content')
    cate_id = request.POST.get('cate_id')
    tags = request.POST.get('tags')
    status = request.POST.get('status')

    if not title or not abstract or not md_content or not html_content or not cate_id or not tags:
        return {'code': 1, 'msg': '请求参数不完整'}
    cate = CateInfo.objects.filter(id=cate_id, status=1).first()
    if not cate:
        return {'code': 1, 'msg': '你选择的类型不存在'}
    tags = tags.split(',')
    if len(tags) == 0:
        return {'code': 1, 'msg': '请为文章选择所属的标签'}
    post.title = title
    post.abstract = abstract
    post.md_content = md_content
    post.html_content = html_content
    post.cate = cate
    post.status = status
    post.logo = logo
    post.update_time = datetime.datetime.now()
    for tag_id in tags:
        tag = TagInfo.objects.filter(id=tag_id, status=1).first()
        if tag:
            post.tags.add(tag)
    post.save()
    return {'code': 0}


def get_post(request):
    id = request.GET.get('id')
    if not id:
        return {'code': 1, 'msg': '请传入文章的id'}
    post = PostInfo.objects.filter(id=id, status=1).first()
    if request.session.get('user'):
        post = PostInfo.objects.filter(author_id=request.session['user'], id=id).first()

    if not post:
        return {'code': 1, 'msg': '文章不存在'}
    md_content = post.md_content if post else ''
    tag_list = post.tags.filter(status=1)
    tags = []
    for tag in tag_list:
        tags.append({'tag_id': tag.id, 'tag_name': tag.name})

    data = ({'id': post.id, 'title': post.title, 'abstract': post.abstract, 'logo': post.logo,
             'cate_id': post.cate.id, 'cate_name': post.cate.name,
             'html_content': post.html_content, 'md_content': md_content,
             'create_time': str(post.create_time), 'update_time': str(post.update_time),
             'tags': tags})
    return {'code': 0, 'data': data}


def get_post_list(request):
    page_size = request.GET.get('size', 5)
    page_num = request.GET.get('num', 1)
    post_list = PostInfo.objects.filter(status=1).order_by('-create_time')
    if request.session.get('user'):
        post_list = PostInfo.objects.filter(author_id=request.session['user'])
    cate_id = request.GET.get('cate_id')
    tag_id = request.GET.get('tag_id')
    keyword = request.GET.get('keyword')

    # 生成paginator对象,定义每页显示page_size条记录
    paginator = Paginator(post_list, page_size)
    # 把当前的页码数转换成整数类型
    currentPage = int(page_num)
    total_num = post_list.count()
    page_nums = int(paginator.num_pages)
    try:
        post_list = paginator.page(page_num).object_list  # 获取当前页码的记录
    except PageNotAnInteger:
        post_list = paginator.page(1).object_list  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages).object_list  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    subject = ''
    if cate_id:
        post_list = PostInfo.objects.filter(status=1).order_by('-create_time')
        cate = CateInfo.objects.filter(id=cate_id, status=1).first()
        if not cate:
            return {'code': 1, 'msg': '类型不存在'}
        post_list = post_list.filter(cate=cate)
        subject = cate.name + ' : ' + str(post_list.count())
    if tag_id:
        post_list = PostInfo.objects.filter(status=1).order_by('-create_time')
        tag = TagInfo.objects.filter(id=tag_id, status=1).first()
        if not tag:
            return {'code': 1, 'msg': '标签不存在'}
        post_list = tag.postinfo_set.filter(status=1)
        subject = 'tag : ' + tag.name
    if keyword:
        subject = 'search : ' + keyword
        post_list = PostInfo.objects.filter(status=1).filter(
            Q(html_content__icontains=keyword) | Q(title__icontains=keyword)).order_by('-create_time')
    data = []
    for post in post_list:
        data.append({'id': post.id, 'title': post.title, 'abstract': post.abstract, 'logo': post.logo,
                     'cate_id': post.cate.id, 'cate_name': post.cate.name, 'author': post.author.username,
                     'create_time': str(post.create_time), 'update_time': str(post.update_time)})
    return {'code': 0, 'data': {'subject': subject, 'total': total_num, 'num_pages': page_num, 'list': data}}


def get_cate_post(request):
    cate_list = CateInfo.objects.filter(status=1)
    data = []
    for cate in cate_list:
        post_list = PostInfo.objects.filter(cate=cate, status=1)
        amount = post_list.count()
        post_data = []
        if post_list:
            for post in post_list:
                post_data.append({'id': post.id, 'title': post.title, 'create_time': post.create_time})
            data.append({'name': cate.name, 'amount': amount, 'data': post_data})
    return {'code': 0, 'data': data}


def get_archive_post(request):
    start_dt = datetime.datetime(2017, 12, 1)
    end_dt = datetime.datetime.now()
    year = end_dt.year + 1 if end_dt.month == 12 else end_dt.year
    month = 1 if end_dt.month == 12 else end_dt.month + 1
    end_dt = datetime.datetime(year, month, 1)
    data = []
    while start_dt.year != end_dt.year and start_dt.month != end_dt.month:
        post_list = PostInfo.objects.filter(create_time__startswith=str(start_dt.strftime('%Y-%m')), status=1)
        amount = post_list.count()
        post_data = []
        for post in post_list:
            post_data.append({'id': post.id, 'title': post.title, 'create_time': str(post.create_time)})
        data.append({'date': str(start_dt.strftime('%Y-%m')), 'amount': amount, 'posts': post_data})
        year = start_dt.year + 1 if start_dt.month == 12 else start_dt.year
        month = 1 if start_dt.month == 12 else start_dt.month + 1
        start_dt = datetime.datetime(year, month, 1)
    return {'code': 0, 'data': data}


def upload_img(request):
    image = request.FILES['file']
    ret, info = qiniu_upload(image.read(), prefix='post_image', mime_type=image.content_type)
    if not ret:
        print(info)
        raise Exception('七牛上传失败')
    return {'code': 0, 'data': settings.QINIU['url'] + ret['key']}
