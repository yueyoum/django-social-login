# -*- coding: utf-8 -*-
from django.db import models

from .app_settings import SOCIAL_LOGIN_UID_LENGTH, SOCIAL_LOGIN_USER_INFO_MODEL
from .manager import SocialUserManager



class User(models.Model):
    is_social = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return '<User %d>' % self.id
    
    
    @property
    def user_info_model(self):
        return models.get_model(*SOCIAL_LOGIN_USER_INFO_MODEL.split('.'))
    
    @property
    def info(self):
        return self.user_info_model.get(id=self.id)
    

    def info_list(self, *args):
        info = self.user_info_model.objects.filter(id=self.id)[0:1].values_list(*args)
        return info[0] if info else info
    
    def get_social_info(self):
        return SocialUser.objects.get(id=self.id)




class SocialUser(models.Model):
    site_uid = models.CharField(max_length=SOCIAL_LOGIN_UID_LENGTH)
    site_id = models.SmallIntegerField()
    
    objects = SocialUserManager()
    
    class Meta:
        unique_together = (('site_uid', 'site_id'),)
        
