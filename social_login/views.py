# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response

from django.conf import settings

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError

from .models import SocialUser


SOCIALOAUTH_SITES = getattr(settings, 'SOCIALOAUTH_SITES', None)
if SOCIALOAUTH_SITES is None:
    raise Exception("SOCIALOAUTH_SITES settings not found!")

socialsites.config(SOCIALOAUTH_SITES)


from .app_settings import (
    SOCIAL_LOGIN_DONE_REDIRECT_URL,
    SOCIAL_LOGIN_ERROR_REDIRECT_URL,
)



def social_login_callback(request, sitename):
    code = request.GET.get('code', None)
    if not code:
        # error occurred
        print 'no code'
        return HttpResponseRedirect(SOCIAL_LOGIN_ERROR_REDIRECT_URL)
    
    s = import_oauth_class(socialsites[sitename])()
    
    try:
        s.get_access_token(code)
    except SocialAPIError:
        # see social_oauth example and docs
        print 'get_access_token error'
        return HttpResponseRedirect(SOCIAL_LOGIN_ERROR_REDIRECT_URL)
    
    if SocialUser.get_user(s.uid, s.site_id) is None:
        SocialUser.create_user(
            username=s.name,
            site_uid=s.uid,
            site_id=s.site_id,
            avatar=s.avatar
        )
    
    # done
    return HttpResponseRedirect(SOCIAL_LOGIN_DONE_REDIRECT_URL)
