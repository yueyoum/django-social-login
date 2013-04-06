# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from social_login.models import SiteUser
from socialoauth import socialsites
from socialoauth.utils import import_oauth_class

from .models import UserAuth, UserInfo


class RegisterLoginError(Exception):
    pass



def home(request):
    if request.siteuser:
        if not UserInfo.objects.filter(user_id=request.siteuser.id).exists():
        #if not request.siteuser.user_info:
            return HttpResponseRedirect(reverse('register_step_2'))
    
    
    all_users = SiteUser.objects.all()
    
    def _make_user_info(u):
        info = {}
        info['id'] = u.id
        info['social'] = u.is_social
        
        if info['social']:
            #social_info = u.get_social_info()
            #site_id = social_info.site_id
            site_id = u.social_user.site_id
            s = import_oauth_class( socialsites.get_site_class_by_id(site_id) )()
            info['social'] = s.site_name_zh
            
        info['username'] = u.user_info.username
        info['avatar'] = u.user_info.avatar
        
        #info['username'], info['avatar'] = u.info_list('username', 'avatar')
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



def register(request):
    if request.method == 'GET':
        return render_to_response(
            'register.html', context_instance=RequestContext(request)
        )
    
    def _register():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterLoginError("Fill email and password")
        
        if UserAuth.objects.filter(email=email).exists():
            raise RegisterLoginError("Email has been taken")
        
        user = UserAuth.objects.create(email=email, password=password)
        return user
    
    try:
        user = _register()
        request.session['uid'] = user.user_id
        return HttpResponseRedirect(reverse('register_step_2'))
    except RegisterLoginError as e:
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
            {'email': UserAuth.objects.get(user_id=request.siteuser.id).email},
            context_instance=RequestContext(request)
        )
    
    def _register_step_2():
        username = request.POST.get('username', None)
        if not username:
            raise RegisterLoginError("Fill in username")
        
        UserInfo.objects.create(user_id=request.siteuser.id, username=username)
        
    try:
        _register_step_2()
        return HttpResponseRedirect(reverse('home'))
    except RegisterLoginError as e:
        return render_to_response(
            'register_step_2.html',
            {
                'email': UserAuth.objects.get(user_id=request.siteuser.id).email,
                'error_msg': e
            },
            context_instance=RequestContext(request)
        )





def login(request):
    if request.siteuser:
        # already logged in
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    
    def _login():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterLoginError("Fill email and password")
        
        if not UserAuth.objects.filter(email=email, password=password).exists():
            raise RegisterLoginError("Invalid account")
        
        user = UserAuth.objects.get(email=email, password=password)
        return user
    
    try:
        user = _login()
        request.session['uid'] = user.user_id
        return HttpResponseRedirect(reverse('home'))
    except RegisterLoginError as e:
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




def login_error(request):
    return HttpResponse("OAuth Failure!")
