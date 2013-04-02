# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from social_login.models import SocialUser


def home(request):
    all_users = SocialUser.objects.select_related('user').all()
    
    def set_current(u):
        current = request.user.is_authenticated() and request.user.id == u.user.id
        u.current = current
        
    for u in all_users:
        set_current(u)
    
    return render_to_response(
        'home.html',
        {'users': all_users},
        context_instance=RequestContext(request)
    )


def login(request):
    return render_to_response('login.html', context_instance=RequestContext(request))
