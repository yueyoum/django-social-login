from django.db import models

from social_login.abstract_models import (
    AbstractBaseSiteUser,
    AbstractInnerUserAuth,
    AbstractUserInfo,
)


class UserAuth(AbstractInnerUserAuth):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    

class UserInfo(AbstractUserInfo):
    pass


# If you wanna extend the default SiteUser fields
# just inherit it, and adding your extra fields like bellow:
#
#class MyCustomSiteUser(AbstractBaseSiteUser):
#   ...
#   ...
#    
#    class Meta:
#        abstract = True

# finally, add SOCIAL_LOGIN_ABSTRACT_SITEUSER = 'app.MyCustomSiteUser'
# in settings.py

