# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.db.models import get_model

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError

from .models import SocialUser


from .app_settings import (
    SOCIALOAUTH_SITES,
    SOCIAL_LOGIN_USER_INFO_MODEL,
    SOCIAL_LOGIN_DONE_REDIRECT_URL,
    SOCIAL_LOGIN_ERROR_REDIRECT_URL,
)


socialsites.config(SOCIALOAUTH_SITES)


def social_login_callback(request, sitename):
    code = request.GET.get('code', None)
    if not code:
        # Maybe user not authorize
        return HttpResponseRedirect(SOCIAL_LOGIN_ERROR_REDIRECT_URL)
    
    s = import_oauth_class(socialsites[sitename])()
    
    try:
        s.get_access_token(code)
    except SocialAPIError:
        # see social_oauth example and docs
        return HttpResponseRedirect(SOCIAL_LOGIN_ERROR_REDIRECT_URL)
    
    
    try:
        user = SocialUser.objects.get(site_uid=s.uid, site_id=s.site_id)
    except SocialUser.DoesNotExist:
        user = SocialUser.objects.create(site_uid=s.uid, site_id=s.site_id)
        info_model = get_model(*SOCIAL_LOGIN_USER_INFO_MODEL.split('.'))
        info_model.objects.create(
            id=user.id,
            username=s.name,
            avatar=s.avatar
        )
        
    # set uid in session, then next time, will auto loggin
    request.session['uid'] = user.id
    
    # done
    return HttpResponseRedirect(SOCIAL_LOGIN_DONE_REDIRECT_URL)

