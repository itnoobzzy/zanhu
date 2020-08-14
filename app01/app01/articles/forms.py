#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/14 11:03
# @Author : zhouzy_a
# @Version：V 0.1
# @File : forms.py
# @desc :发布文章的form表单

from django import forms

from app01.articles.models import Article

from markdownx.fields import MarkdownxFormField


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput)
    edited = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=False)
    content = MarkdownxFormField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'tags', 'status', 'edited']
