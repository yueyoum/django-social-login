# -*- coding: utf-8 -*-

from django.conf import settings


SOCIAL_LOGIN_USER_MODEL = getattr(settings, 'SOCIAL_LOGIN_USER_MODEL', 'auth.User')
SOCIAL_LOGIN_UID_LENGTH = getattr(settings, 'SOCIAL_LOGIN_UID_LENGTH', 255)

SOCIAL_LOGIN_ENABLE_ADMIN = getattr(settings, 'SOCIAL_LOGIN_ENABLE_ADMIN', True)

SOCIAL_LOGIN_LOGIN_TEMPLATE = getattr(
    settings, 'SOCIAL_LOGIN_LOGIN_TEMPLATE', 'login.html'
)

SOCIAL_LOGIN_LOGIN_URL = getattr(
    settings, 'SOCIAL_LOGIN_LOGIN_URL', r'^account/login/?$'
)

SOCIAL_LOGIN_CALLBACK_URL_PATTERN = getattr(
    settings, 'SOCIAL_LOGIN_CALLBACK_URL_PATTERN', r'^account/oauth/(?P<sitename>\w+)/?$'
)

SOCIAL_LOGIN_DONE_REDIRECT_URL = getattr(
    settings, 'SOCIAL_LOGIN_DONE_REDIRECT_URL', '/'
)

SOCIAL_LOGIN_ERROR_REDIRECT_URL = getattr(
    settings, 'SOCIAL_LOGIN_ERROR_REDIRECT_URL', '/login/error'
)

