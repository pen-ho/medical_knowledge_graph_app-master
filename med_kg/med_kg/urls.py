"""med_kg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
sys.path.append("../../")

from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from med_kg import index_view
from med_kg import ner_view
from med_kg import relation_view
from med_kg import question_answering

'''
urlpatterns 是一个路由-视图函数映射关系的列表,此列表的映射关系由url函数来确定
    url() 函数
        用于描述路由与视图函数的对应关系
        模块
        from django.conf.urls import url
        语法:
        url(regex, views, name=None)
        参数：
        regex: 字符串类型，匹配的请求路径，允许是正则表达式
        views: 指定路径所对应的视图处理函数的名称
        name: 为地址起别名，在模板中地址反向解析时使用
        每个正则表达式前面的r表示'\'不转义的原始字符串
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index_view.index),
    url(r'^ner-post', ner_view.ner_post),
    url(r'^search_entity', relation_view.search_entity),
    url(r'^search_relation', relation_view.search_relation),
    # url(r'^qa', question_answering.question_answering),
    url(r'^qa', question_answering.question_answering_med),  # hzp
]
