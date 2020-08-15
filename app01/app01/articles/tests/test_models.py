#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/15 13:16
# @Author : zhouzy_a
# @Version：V 0.1
# @File : test_models.py
# @desc :文章模块的模型类测试

from test_plus.test import TestCase

from app01.articles.models import Article


class ArticlesModelsTest(TestCase):
    """文章模块模型类测试"""

    def setUp(self) -> None:
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="程序员梦工场",
            status="P",
            user=self.user
        )
        self.not_p_article = Article.objects.create(
            title="第二篇文章",
            content="慕课网-程序员的梦工厂",
            user=self.user
        )

    def test_object_instance(self):
        """判断实例对象是否为Article类型"""
        assert isinstance(self.article, Article)
        assert isinstance(self.not_p_article, Article)
        assert isinstance(Article.objects.get_published()[0], Article)

    def test_return_values(self):
        """测试返回值"""
        assert self.article.status == "P"
        # assert self.article.status != "P"
        assert self.not_p_article.status == "D"
        assert str(self.article) == "第一篇文章"
        assert self.article in Article.objects.get_published()
        assert Article.objects.get_published()[0].title == "第一篇文章"
        assert self.not_p_article in Article.objects.get_drafts()














