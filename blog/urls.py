#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://127.0.0.1:8000/blog/
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type")

]
