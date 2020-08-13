#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/13 13:47
# @Author : zhouzy_a
# @Version：V 0.1
# @File : test_urls.py
# @desc :测试动态视图的url

from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestNewsURLs(TestCase):
    """动态"""

    def setUp(self) -> None:
        self.user = self.make_user()

    def test_list_reverse(self):
        """正向解析动态列表页"""
        self.assertEqual(reverse('news:list'), '/news/')

    def test_list_resolve(self):
        """反向解析动态列表页"""
        self.assertEqual(resolve('/news/').view_name, 'news:list')

    def test_post_news_reverse(self):
        """正向解析发表动态"""
        self.assertEqual(reverse('news:post_news'), '/news/post-news/')

    def test_post_news_resolve(self):
        """反向解析发表动态"""
        self.assertEqual(resolve('/news/post-news/').view_name, 'news:post_news')

    def test_delete_reverse(self):
        """正向解析删除动态"""
        self.assertEqual(reverse('news:delete_news', kwargs={'pk': 1}), '/news/delete/1/')

    def test_delete_resolve(self):
        """反向解析删除动态"""
        self.assertEqual(resolve('/news/delete/1/').view_name, 'news:delete_news')
