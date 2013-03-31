# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import SocialUser


class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('Username', 'site_uid', 'site_id', 'Avatar')
    list_filter = ('site_id',)
    
    def Username(self, obj):
        return obj.user.username
    
    def Avatar(self, obj):
        return '<img src="%s" />' % obj.avatar
    Avatar.allow_tags = True
    
    
admin.site.register(SocialUser, SocialUserAdmin)