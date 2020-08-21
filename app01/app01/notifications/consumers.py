#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    """处理通知应用中的WebSocket请求"""

    def connect(self):
        """建立连接"""
        if self.scope['user'].is_anonymous:
            # 未登录用户拒接连接
            self.close()
        else:
            self.channel_layer.group_add('notifications', self.channel_name)
            self.accept()

    def receive(self, text_data=None, bytes_data=None):
        """接收到的消息返回给前端"""
        recipient = self.scope['user'].username
        # news动态发布时通知所有在线用户
        if text_data.get('key') == "additional_news":
            self.send(text_data=json.dumps(text_data))
        # 只通知接收者，即recipient == 动作对象的作者
        if recipient != text_data.get("actor_name") and recipient == text_data.get("action_object"):
            self.send(text_data=json.dumps(text_data))

    def disconnect(self, code):
        """断开连接"""
        self.channel_layer.group_discard('notifications', self.channel_name)
