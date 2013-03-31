# -*- coding:utf-8 -*-

from django.conf import settings
from social_login import app_settings


class SocialLoginSettings(object):
    def __getattr__(self, name):
        value = getattr(settings, name, None)
        if value is not None:
            return value
        
        value = getattr(app_settings, name, None)
        if value is not None:
            return value
        
        raise Exception("No settings for %s" % name)
    


social_login_settings = SocialLoginSettings()