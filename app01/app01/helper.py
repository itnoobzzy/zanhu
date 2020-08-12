#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/12 16:00
# @Author : zhouzy_a
# @Version：V 0.1
# @File : helper.py
# @desc :自定义装饰器

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View


def ajax_required(f):
    """验证是否为AJAX请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是ajax请求")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):
    """
    验证是否为原作者，用于状态删除、文章编辑
    个人中心模块中更新信息不用验证是否为原作者，因为UserUpdateView返回的是当前登录用户的form
    """
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)
