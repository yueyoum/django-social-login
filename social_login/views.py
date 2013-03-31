# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect

from django.conf import settings

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError

from social_login.models import SocialUser


SOCIALOAUTH_SITES = getattr(settings, 'SOCIALOAUTH_SITES', None)
if SOCIALOAUTH_SITES is None:
    raise Exception("SOCIALOAUTH_SITES settings not found!")

socialsites.config(SOCIALOAUTH_SITES)


def login(request):
    if request.method == 'GET':
        # show the login page
        
        def _link(s):
            s = import_oauth_class(s)()
            link = '使用 %s 登录' % s.site_name
            
            return """<div style="margin: 20px;">
            <a href="%s">%s</a>
            </div>""" % (s.authorize_url, link)
            
        links = map(_link, socialsites.list_sites())
        links = '\n'.join(links)
        
        html = """<!DOCTYPE html>
        <html>
            <body>%s</body>
        </html>
        """ % links
        
        return HttpResponse(html)


def oauth_callback(request, sitename):
    code = request.GET.get('code', None)
    if not code:
        # error occurred
        raise Exception("get code error")
    
    s = import_oauth_class(socialsites[sitename])()
    
    s.get_access_token(code)
    
    SocialUser.create_user(
        username=s.name,
        site_uid=s.uid,
        site_id=s.site_id,
        avatar=s.avatar
    )
    
    print 'done...'
    return HttpResponse('ok')
    
