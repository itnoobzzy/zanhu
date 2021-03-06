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
        return News.objects.filter(reply=False).select_related('user', 'parent').prefetch_related('liked')


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


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """点赞， AJAX POST请求"""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({'likes': news.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """
    返回动态的评论,AJAX GET请求
    1.
    """
    news_id = request.GET['news']
    news = News.objects.select_related('user').get(pk=news_id)
    news_html = render_to_string("news/news_single.html", {"news": news})
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """
    发布评论， AJAX POST 请求
    1. 获取评论的动态id,评论内容
    2. 使用News模型类的reply_this方法更新评论
    3. 返回评论数量
    """
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_required
@require_http_methods(['POST'])
def update_interactions(request):
    """更新互动信息"""
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    return JsonResponse({'likes': news.count_likers(), 'comments': news.comment_count()})
