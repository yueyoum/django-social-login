from django.db import models
from social_login.models import AbstractInnerUserAuth, AbstractUserInfo


class UserAuth(AbstractInnerUserAuth):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    

class UserInfo(AbstractUserInfo):
    pass
