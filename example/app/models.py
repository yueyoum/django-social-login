from django.db import models


from social_login.manager import InnerUserManager


class UserAuth(models.Model):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    objects = InnerUserManager()
    
    
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    avatar = models.CharField(max_length=255, blank=True)
    
