# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import home, login

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    url(r'^account/login/?', login, name="login"),
)