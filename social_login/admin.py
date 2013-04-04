# -*- coding: utf-8 -*-
from .app_settings import SOCIAL_LOGIN_ENABLE_ADMIN, SOCIAL_LOGIN_USER_INFO_MODEL

if SOCIAL_LOGIN_ENABLE_ADMIN:
    from django.contrib import admin
    from django.db.models import get_model
    from .models import SocialUser
    
    info_model = get_model(*SOCIAL_LOGIN_USER_INFO_MODEL.split('.'))
    class SocialUserAdmin(admin.ModelAdmin):
        list_display = ('id', 'Username', 'site_uid', 'site_id', 'Avatar')
        list_filter = ('site_id',)
        
        def Username(self, obj):
            return info_model.objects.get(id=obj.id).username
        
        def Avatar(self, obj):
            return '<img src="%s" />' % info_model.objects.get(id=obj.id).avatar
        Avatar.allow_tags = True
        
        
    admin.site.register(SocialUser, SocialUserAdmin)
