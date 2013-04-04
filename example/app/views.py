# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from social_login.models import User

from .models import UserAuth, UserInfo

def home(request):
    if request.siteuser:
        if not UserInfo.objects.filter(id=request.siteuser.id).exists():
            return HttpResponseRedirect(reverse('register_step_2'))
    
    
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


class RegisterError(Exception):
    pass


def register(request):
    if request.method == 'GET':
        return render_to_response(
            'register.html', context_instance=RequestContext(request)
        )
    
    def _register():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterError("Fill email and password")
        
        if UserAuth.objects.filter(email=email).exists():
            raise RegisterError("Email has been taken")
        
        user = UserAuth.objects.create(email=email, password=password)
        return user
    
    try:
        user = _register()
        request.session['uid'] = user.id
        return HttpResponseRedirect(reverse('register_step_2'))
    except RegisterError as e:
        return render_to_response(
            'register.html',
            {'error_msg': e},
            context_instance=RequestContext(request)
        )
    



def register_step_2(request):
    if not request.siteuser:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'GET':
        return render_to_response(
            'register_step_2.html',
            {'email': UserAuth.objects.get(id=request.siteuser.id).email},
            context_instance=RequestContext(request)
        )
    
    def _register_step_2():
        username = request.POST.get('username', None)
        if not username:
            raise RegisterError("Fill in username")
        
        UserInfo.objects.create(id=request.siteuser.id, username=username)
        
    try:
        _register_step_2()
        return HttpResponseRedirect(reverse('home'))
    except RegisterError as e:
        return render_to_response(
            'register_step_2.html',
            {
                'email': UserAuth.objects.get(id=request.siteuser.id).email,
                'error_msg': e
            },
            context_instance=RequestContext(request)
        )





def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    
    def _login():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterError("Fill email and password")
        
        if not UserAuth.objects.filter(email=email, password=password).exists():
            raise RegisterError("Invalid account")
        
        user = UserAuth.objects.get(email=email, password=password)
        return user
    
    try:
        user = _login()
        request.session['uid'] = user.id
        return HttpResponseRedirect(reverse('home'))
    except RegisterError as e:
        return render_to_response(
            'login.html',
            {'error_msg': e},
            context_instance=RequestContext(request)
        )



def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('home'))
