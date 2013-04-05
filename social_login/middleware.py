# -*- coding: utf-8 -*-

from django.utils.functional import SimpleLazyObject

from .models import SiteUser

# add 'social_login.middleware.SocialLoginUser' in MIDDLEWARE_CLASSES
# then the request object will has a `siteuser` property
#
# you can using it like this:
# if request.siteuser:
#     # there has a logged user,
#     uid = request.siteuser.id
# else:
#     # no one is logged
#
# Don't worry about the performance,
# `siteuser` is a lazy object, it readly called just access the `request.siteuser`



class SocialLoginUser(object):
    def process_request(self, request):
        def get_user():
            uid = request.session.get('uid', None)
            if not uid:
                return None
            
            return SiteUser.objects.get(id=int(uid))
        
        request.siteuser = SimpleLazyObject(get_user)