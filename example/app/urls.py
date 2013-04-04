# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import home, login, logout

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    url(r'^account/login/?', login, name="login"),
    url(r'^account/logout/?', logout, name="logout"),
)