#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from app01.messager import views

app_name = 'messager'

urlpatterns = [
    path('', views.MessageListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('<username>/', views.ConversationListView.as_view(), name='conversation_detail'),
]
