# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from .app_settings import SOCIAL_LOGIN_UID_LENGTH


class BaseManager(models.Manager):
    def create(self, is_social, **kwargs):
        if 'user' not in kwargs and 'user_id' not in kwargs:
            user = SiteUser.objects.create(is_social=is_social)
            kwargs['user_id'] = user.id
            
        return super(BaseManager, self).create(**kwargs)



class SocialUserManager(BaseManager):
    def create(self, **kwargs):
        return super(SocialUserManager, self).create(True, **kwargs)
        
        
class InnerUserManager(BaseManager):
    def create(self, **kwargs):
        return super(InnerUserManager, self).create(False, **kwargs)
        





def _abstract_siteuser():
    custom_siteuser = getattr(settings, 'SOCIAL_LOGIN_ABSTRACT_SITEUSER', None)
    if not custom_siteuser:
        return AbstractBaseSiteUser
    
    _app, _model = custom_siteuser.split('.')
    _module = __import__('%s.models' % _app, fromlist=[_model])
    _model = getattr(_module, _model)
    if not _model._meta.abstract:
        raise AttributeError("%s must be abstract model" % custom_siteuser)
    return _model


class AbstractBaseSiteUser(models.Model):
    """
    Abstract model for store the common info of social user and inner user.
    You can extend the abstract model like this:
    
    class CustomAbstractSiteUser(AbstractBaseSiteUser):
        # some extra fields...
        
        class Meta:
            abstract = True
            
    then, and your model in settings.py file:
    SOCIAL_LOGIN_ABSTRACT_SITEUSER = 'myapp.CustomAbstractSiteUser'
    """
    is_social = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        abstract = True


class SiteUser(_abstract_siteuser()):
    
    def __unicode__(self):
        return '<SiteUser %d>' % self.id




class SocialUser(models.Model):
    user = models.OneToOneField(SiteUser, related_name='social_user')
    site_uid = models.CharField(max_length=SOCIAL_LOGIN_UID_LENGTH)
    site_id = models.SmallIntegerField()
    
    objects = SocialUserManager()
    
    class Meta:
        unique_together = (('site_uid', 'site_id'),)




# your project's user model must inherit from the following two abstarct model

class AbstractInnerUserAuth(models.Model):
    user = models.OneToOneField(SiteUser, related_name='inner_user')
    objects = InnerUserManager()
    
    class Meta:
        abstract = True
        
        
class AbstractUserInfo(models.Model):
    user = models.OneToOneField(SiteUser, related_name='user_info')
    username = models.CharField(max_length=32)
    avatar = models.CharField(max_length=255, blank=True)
    
    class Meta:
        abstract = True
