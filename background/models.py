import uuid, datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from .utils import qiniu_upload


class UserInfo(models.Model):
    STATUS = (
        (0, '删除'),
        (1, '正常'),
    )
    TYPE = (
        (0, '普通用户'),
        (1, '超级管理员'),
    )
    username = models.CharField(verbose_name='用户名', max_length=50, unique=True)
    password = models.CharField(verbose_name='密码', max_length=50)
    status = models.IntegerField(verbose_name='状态', choices=STATUS, default=1)
    type = models.IntegerField(verbose_name='用户类型', choices=STATUS, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username


class CateInfo(models.Model):
    STATUS = (
        (0, '删除'),
        (1, '正常'),
    )
    name = models.CharField(verbose_name='类型名', max_length=50, unique=True)
    status = models.IntegerField(verbose_name='状态', choices=STATUS, default=1)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class TagInfo(models.Model):
    STATUS = (
        (0, '删除'),
        (1, '正常'),
    )
    name = models.CharField(verbose_name='标签名', max_length=50, unique=True)
    status = models.IntegerField(verbose_name='状态', choices=STATUS, default=1)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class PostInfo(models.Model):
    STATUS = (
        (0, '删除'),
        (1, '正常'),
    )
    title = models.CharField(verbose_name='文章标题', max_length=200, unique=True)
    logo = models.CharField('文章预览图', max_length=128, null=True, blank=True, default='')
    abstract = models.CharField(verbose_name='文章摘要', max_length=300)
    author = models.ForeignKey(UserInfo, verbose_name='文章作者')
    md_content = models.TextField(verbose_name='markdown内容')
    cate = models.ForeignKey(CateInfo, verbose_name='文章类型', on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagInfo, verbose_name='文章标签')
    html_content = models.TextField(verbose_name='文章内容')
    status = models.IntegerField(verbose_name='状态', choices=STATUS, default=1)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)

    def __str__(self):
        return self.title
