from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views import defaults as default_views

from app01.news.views import NewsListView

urlpatterns = [
                  path("", NewsListView.as_view(), name="home"),

                  # 用户管理
                  path("users/", include("app01.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),

                  # 第三方应用
                  path('markdownx/', include('markdownx.urls')),
                  path('comments/', include('django_comments.urls')),

                  # 开发的应用
                  path('news/', include('app01.news.urls', namespace='news')),
                  path('articles/', include('app01.articles.urls', namespace='articles')),
                  path('qa/', include('app01.qa.urls', namespace='qa')),
                  path('messages/', include('app01.messager.urls', namespace='messages')),
                  path('notifications/', include('app01.notifications.urls', namespace='notifications')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
