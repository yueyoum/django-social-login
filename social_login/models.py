from django.db import models

from .app_settings import SOCIAL_LOGIN_USER_MODEL, SOCIAL_LOGIN_UID_LENGTH


class SocialUser(models.Model):
    user = models.OneToOneField(SOCIAL_LOGIN_USER_MODEL, related_name='social_user')
    site_uid = models.CharField(max_length=SOCIAL_LOGIN_UID_LENGTH)
    site_id = models.SmallIntegerField()
    avatar = models.CharField(max_length=255, blank=True)
    
    class Meta:
        unique_together = (('site_uid', 'site_id'),)
        
        
    @classmethod
    def user_model(cls):
        return cls._meta.get_field('user').rel.to
    
    @classmethod
    def create_user(cls, username, site_uid, site_id, avatar='', **kwargs):
        user = cls.user_model().objects.create_user(username=username, **kwargs)
        cls.objects.create(
            user = user,
            site_uid = site_uid,
            site_id = site_id,
            avatar = avatar
        )
        return user
    
    @classmethod
    def get_user(cls, site_uid, site_id):
        try:
            return cls.objects.select_related('user').get(
                site_uid=site_uid, site_id=site_id
            )
        except SocialUser.DoesNotExist:
            return None
    
    
    
