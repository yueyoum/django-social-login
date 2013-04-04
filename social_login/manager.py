# -*- coding: utf-8 -*-

from django.db import models


# custom the register/login User Model,
# the Model MUST using InnerUserManager
#
# example:
# class UserAuth(models.Model):
#     email = models.EmailField()
#     password = models.CharField(max_length=64)
#
#    objects = InnerUserManager()



class BaseManager(models.Manager):
    def create(self, is_social, **kwargs):
        if 'id' not in kwargs:
            m = models.get_model('social_login', 'User')
            u = m.objects.create(is_social=is_social)
            kwargs['id'] = u.id
            
        return super(BaseManager, self).create(**kwargs)
        
        



class SocialUserManager(BaseManager):
    def create(self, **kwargs):
        return super(SocialUserManager, self).create(True, **kwargs)
        
        
class InnerUserManager(BaseManager):
    def create(self, **kwargs):
        return super(InnerUserManager, self).create(False, **kwargs)
        