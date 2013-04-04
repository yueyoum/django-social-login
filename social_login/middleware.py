# -*- coding: utf-8 -*-

from django.utils.functional import SimpleLazyObject

from .models import User


class SocialLoginUser(object):
    def process_request(self, request):
        def get_user():
            uid = request.session.get('uid', None)
            if not uid:
                return None
            
            return User.objects.get(id=int(uid))
        
        request.siteuser = SimpleLazyObject(get_user)