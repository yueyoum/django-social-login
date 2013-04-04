# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import home, login, logout, register, register_step_2

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    url(r'^account/login/?$', login, name="login"),
    url(r'^account/logout/?$', logout, name="logout"),
    url(r'^account/register/?$', register, name="register"),
    url(r'^account/register2/?$', register_step_2, name="register_step_2"),
)