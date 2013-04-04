# -*- coding: utf-8 -*-
from .app_settings import SOCIAL_LOGIN_ENABLE_ADMIN, SOCIAL_LOGIN_USER_INFO_MODEL

if SOCIAL_LOGIN_ENABLE_ADMIN:
    from django.contrib import admin
    from django.db.models import get_model
    from .models import User, SocialUser
    
    info_model = get_model(*SOCIAL_LOGIN_USER_INFO_MODEL.split('.'))
    class UserAdmin(admin.ModelAdmin):
        list_display = ('id', 'Username', 'Avatar', 'is_social', 'is_active',
                        'date_joined', 'SiteId')
        list_filter = ('is_social',)
        
        def Username(self, obj):
            return info_model.objects.get(id=obj.id).username
        
        def Avatar(self, obj):
            return '<img src="%s" />' % info_model.objects.get(id=obj.id).avatar
        Avatar.allow_tags = True
        
        def SiteId(self, obj):
            return SocialUser.objects.get(id=obj.id).site_id
        
        
    admin.site.register(User, UserAdmin)
