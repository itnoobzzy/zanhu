#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'zzy'

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from app01.news.models import News
from app01.helper import ajax_required, AuthorRequiredMixin


class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    paginate_by = 20
    template_name = 'news/news_list.html'

    def get_queryset(self, *args, **kwargs):
        return News.objects.filter(reply=False)


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """继承DeleteView重写delete方法， 使用ajax请求"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy("news:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    """发送动态，AJAX POST 请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容为空！")
