# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from social_login.models import User


def home(request):
    all_users = User.objects.all()
    
    def _make_user_info(u):
        info = {}
        info['id'] = u.id
        info['is_social'] = u.is_social
        info['username'], info['avatar'] = u.info_list('username', 'avatar')
        info['current'] = request.siteuser and request.siteuser.id == u.id
        return info
    
    users = map(_make_user_info, all_users)
    
    
    return render_to_response(
        'home.html',
        {
            'users': users,
            'logged': request.siteuser
        },
        context_instance=RequestContext(request)
    )


def login(request):
    return render_to_response('login.html', context_instance=RequestContext(request))



def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('home'))
