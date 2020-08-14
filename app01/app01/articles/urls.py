#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from app01.articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='list'),
    path('write-new-article/', views.CreateArticleView.as_view(), name='write_new'),
    path('drafts/', views.DraftsListView.as_view(), name='drafts'),

]
