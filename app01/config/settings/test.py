"""
With these settings, tests run faster.
"""

# from .base import *  # noqa
# from .base import env
#
# # GENERAL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECRET_KEY = env(
#     "DJANGO_SECRET_KEY",
#     default="MZVIRdH7uzMp9jDnYSc8iXgSsNUhOKFazWBPo2wFOxZQAfqPPaXtn5uekpiOhWd6",
# )
# # https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
# TEST_RUNNER = "django.test.runner.DiscoverRunner"
#
# # CACHES
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "",
#     }
# }
#
# # PASSWORDS
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
# PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
#
# # TEMPLATES
# # ------------------------------------------------------------------------------
# TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
#     (
#         "django.template.loaders.cached.Loader",
#         [
#             "django.template.loaders.filesystem.Loader",
#             "django.template.loaders.app_directories.Loader",
#         ],
#     )
# ]
#
# # EMAIL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
#
#
# # Your stuff...
# # ------------------------------------------------------------------------------


class A():
    def who_am_i(self):
        print("I am A")


class B(A):
    pass


class C(A):
    def who_am_i(self):
        print("I am C")


class D(B, C):
    pass


d = D()

print(d.who_am_i())
