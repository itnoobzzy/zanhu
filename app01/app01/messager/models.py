#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'zzy'


from __future__ import unicode_literals
import uuid

# from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


# @python_2_unicode_compatible
class MessageQuerySet(models.query.QuerySet):
    """私信查询集"""

    def get_conversation(self, sender, recipient):
        """
        获取私信内容
        :param sender: 发送者,发送者既可以是当前登录用户也可以是私信对象
        :param recipient: 接受者，接收者即可以是当前登录用户也可以是私信对象
        :return: 并集后的查询集（私信内容）
        """
        qs_one = self.filter(sender=sender, recipient=recipient).select_related('sender', 'recipient')  # A发送给B的消息
        qs_two = self.filter(sender=recipient, recipient=sender).select_related('sender', 'recipient')  # B发送给A的消息
        return qs_one.union(qs_two).order_by('created_at')  # 取并集后按时间排序

    def get_most_recent_conversation(self, recipient):
        """
        获取当前登录用户的最后一条私信的对象
        1. 获取当前登录用户的最后一条私信
        2. 如果当前用户有发送消息，返回消息的接收者
            如果当前用户没有发送消息，返回消息的发送者
            否则表示当前用户没有私信，返回当前用户
        :param recipient: 当前登录用户
        :return: 返回当前登录用户最后一条私信的对象
        """
        try:
            qs_sent = self.filter(sender=recipient).select_related('sender', 'recipient')  # 当前登录用户发送的消息
            qs_received = self.filter(recipient=recipient).select_related('sender', 'recipient')  # 当前登录用户接收的消息
            qs = qs_sent.union(qs_received).latest("created_at")  # 最后一条消息
            if qs.sender == recipient:
                # 如果当前登录用户有发送消息，返回消息的接收者
                return qs.recipient
            return qs.sender
        except self.model.DoesNotExist:
            # 如果模型实例不存在， 则返回当前用户
            return get_user_model().objects.get(username=recipient.username)


# @python_2_unicode_compatible
class Message(models.Model):
    """私信模型类"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_message',
                               blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, verbose_name='是否未读')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
