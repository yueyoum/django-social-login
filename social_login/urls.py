# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url


from social_login.views import login, oauth_callback

urlpatterns = patterns('',
    url(r'^login/?$', login, name='login'),
    url(r'^oauth/(?P<sitename>\w+)/?$', oauth_callback, name='oauth_callback'),
)