#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'zzy'

from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_comments.signals import comment_was_posted

from app01.helper import AuthorRequiredMixin
from app01.articles.models import Article
from articles.forms import ArticleForm
from app01.notifications.views import notification_handler


class ArticlesListView(LoginRequiredMixin, ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 20
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()


class DraftsListView(ArticlesListView):
    """草稿箱文章列表"""

    def get_queryset(self, **kwargs):
        # 当前用户的草稿
        return Article.objects.filter(user=self.request.user).get_drafts()


class CreateArticleView(LoginRequiredMixin, CreateView):
    """发表文章"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = "您的文章已创建成功！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """创建成功跳转url"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy('articles:list')
        # return reverse('articles:list')


class DetailArticleView(LoginRequiredMixin, DetailView):
    """文章详情"""
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        return Article.objects.select_related('user').filter(slug=self.kwargs['slug'])


class ArticleEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """文章的编辑功能"""
    model = Article
    messages = "您的文章编辑成功！"
    form_class = ArticleForm
    template_name = 'articles/article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        """编辑成功后跳转"""
        messages.success(self.request, self.messages)
        return reverse("articles:list", kwargs={"slug": self.get_object().slug})


def notify_comment(**kwargs):
    """文章有评论时通知作者"""
    actor = kwargs['request'].user
    obj = kwargs['comments'].content_object

    notification_handler(actor, obj.user, 'C', obj)


comment_was_posted.connect(receiver=notify_comment)
