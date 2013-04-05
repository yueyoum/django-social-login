# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),
    url(r'^account/login/?$', views.login, name="login"),
    url(r'^account/logout/?$', views.logout, name="logout"),
    url(r'^account/register/?$', views.register, name="register"),
    url(r'^account/register2/?$', views.register_step_2, name="register_step_2"),
    url(r'^account/login/error/?$', views.login_error, name="login_error"),
)