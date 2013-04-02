# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url


from .views import social_login_callback
from .app_settings import SOCIAL_LOGIN_CALLBACK_URL_PATTERN


urlpatterns = patterns('',
    url(SOCIAL_LOGIN_CALLBACK_URL_PATTERN,
        social_login_callback,
        name='social_login_callback'),
)