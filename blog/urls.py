"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from background.controllers import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # account
    url(r'^login/?$', account.login),
    url(r'^logout/?$', account.logout),
    url(r'^register/?$', account.register),

    # tag
    url(r'^tag/add/?$', tag.add_tag),
    url(r'^tag/list/?$', tag.get_tag_list),
    url(r'^tag/get/?$', tag.get_tag),
    url(r'^tag/delete/?$', tag.delete_tag),
    url(r'^tag/modify/?$', tag.modify_tag),

    # cate
    url(r'^cate/add/?$', cate.add_cate),
    url(r'^cate/list/?$', cate.get_cate_list),
    url(r'^cate/get/?$', cate.get_cate),
    url(r'^cate/delete/?$', cate.delete_cate),
    url(r'^cate/modify/?$', cate.modify_cate),

    # post
    url(r'^post/add/?$', post.add_post),
    url(r'^post/list/?$', post.get_post_list),
    url(r'^post/get/?$', post.get_post),
    url(r'^post/delete/?$', post.delete_post),
    url(r'^post/modify/?$', post.modify_post),
    url(r'^post/cate_post/?$', post.get_cate_post),
    url(r'^post/archive/?$', post.get_archive_post),
    url(r'^post/img_upload/?$', post.upload_img),

]
