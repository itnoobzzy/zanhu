#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'zzy'
from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestUserURLs(TestCase):
    """用户 """

    def setUp(self) -> None:
        self.user = self.make_user()

    def test_detail_reverse(self):
        """正向解析用户详情url"""
        self.assertEqual(reverse('users:detail', kwargs={'username': 'testuser'}), '/users/testuser/')

    def test_detail_resolve(self):
        """反向解析用户详情url"""
        self.assertEqual(resolve('/users/testuser/').view_name, 'users:detail')

    def test_update_reverse(self):
        """正向解析用户更新url"""
        self.assertEqual(reverse('users:update'), '/users/update/')

    def test_update_resoleve(self):
        """反向解析用户更新url"""
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')
