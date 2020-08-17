#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/14 11:03
# @Author : zhouzy_a
# @Version：V 0.1
# @File : forms.py
# @desc :问答模块的form表单

from django import forms

from markdownx.fields import MarkdownxFormField

from app01.qa.models import Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput)
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags', 'status']
