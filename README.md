# django-social-login


用第三方帐号登录网站

## Usage

### install

```bash
pip install django-social-login
```
    
    
### settings.py

下面几项是必要的设置，必须在项目 settings.py 中设置好。
此外还有一些非必要的设置，[见这里](#optional-settings)

*   **把 `social_login` 加入到 `INSTALLED_APPS` 中**

*   **设置项目urls.py**

    把 `url(r'', include('social_login.urls'))` 放到 项目urls.py 的 **最下面**
    
    ```python
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        # ...
        url(r'', include('social_login.urls')),
    )
    ```
    

*   **SOCIALOAUTH_SITES**
    
    要使用的提供OAuth2服务的站点信息，见 [socialoauth文档][1]

*   **SOCIAL_LOGIN_USER_INFO_MODEL**

    用户信息的model，例如你的app名叫 myapp， 存储用户信息的model叫 UserInfo,
    那么这里就设置为 `SOCIAL_LOGIN_USER_INFO_MODEL='myapp.UserInfo'`
    
    用户信息表的定义见下面的 [说明](#modelspy)
    
    

*   **SOCIAL_LOGIN_ERROR_REDIRECT_URL**

    在用户认证过程中发生错误（用户拒绝授权等）时要跳转到的url
    
    
    
*   **'social_login.context_processors.social_sites'**

    把它加入到 **TEMPLATE_CONTEXT_PROCESSORS** 中，
    并且在 views 中传递了 `context_instance`，
    那么在模板中就可以通过 `{% for s in social_sites %}` 的形式在获得配置的站点信息
    
        s.site_id       在 SOCIALOAUTH_SITES 中配置的 site_id
        s.site_name     站点的 英文名字
        s.site_name_zh  中文名字
        s.authorize_url 引导用户授权的url
        
    
    
*   **'social_login.middleware.SocialLoginUser'**

    把它加入到 **MIDDLEWARE_CLASSES** 中，
    这样在每个 view 的 `request` 对象会有一个 `siteuser` 属性
    
    如果设置了 siteuser.is_active = False，那么此用户是无法登录的,
    `request.siteuser` 判断为None
    
    可以通过 `if request.siteuser` 来判断是否有用户登录。
    如果有 那么 `request.siteuser` 是一个 `social_login.SiteUser` 对象
    
    可以通过一下方法访问其属性：
    
        request.siteuser.id                     用户uid
        request.siteuser.is_social              是否是第三方帐号
        request.siteuser.date_joined            用户加入时间
        request.siteuser.user_info.XX           用户信息表中的XX列
        
        request.siteuser.inner_user.XX          XX是定义在自身网站用户登录认证表中的field
        
        # if request.siteuser.is_social is True
        request.siteuser.social_user.site_uid   用户第三方站点中的uid
        request.siteuser.social_user.site_id    用户来自哪个网站的site_id
    
    
    
### models.py

你的项目至少需要定义两个用户表:

*   自身网站注册用户的认证表    - 用来保存自身注册用户
*   用户信息表                 - 保存所有用户信息。
    
example:

```python

from social_login.abstract_models import AbstractInnerUserAuth, AbstractUserInfo

class UserAuth(AbstractInnerUserAuth):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    
class UserInfo(AbstractUserInfo):
    pass
```

对于 `AbstractInnerUserAuth` 和 `AbstractUserInfo` 的定义可以直接看
[源码](blob/master/social_login/abstract_models.py)
    
    
此外，你还可以 **扩展** siteuser 表，只要自己定义的表 继承自
`social_login.abstract_models.AbstractBaseSiteUser` 并且 设置了 `abstract = True`
，然后在 settings.py 加入
`SOCIAL_LOGIN_ABSTRACT_SITEUSER = 'yourapp.YourCustomAbstractSiteUser'` 即可
可以参考 [example/app/models.py](blob/master/example/app/models.py)
最下面注释掉的部分
    
    
    
    
经过上面的设置后， `python manage.py validate` 无错误就 `python manage.py syncdb`,
`python manage.py runserver`.
如果有错，请确保正确安装，并且正确设置。完整的例子请参考 `example`
    
    
## Login process

第三方登录和自己网站内部注册/登录的流程如下：

*   当用户点击login后，提供两个选择：
    
    *   使用已经注册的帐号登录
    *   使用第三方帐号登录
    
    ![login][2]
    
*   用户可以先 注册 ，并且用此帐号登录，也可以用第三方帐号登录。

    登录一些用户后的状态如下图：
    
    图中显示了登录过的用户信息，注意 uid为 5 和 6 的用户，
    他们来自不同的网站，但用户名却相同。
    所以在上面的设置中 `username` 不能设置为 `unique=True`
    
    ![status][3]
    

完整的流程可以 运行 `example` 中的项目


## Optional Settings

#### SOCIAL_LOGIN_UID_LENGTH

保存用户第三方站点uid的Field是一个 CharField，这个设置用来指定此 CharField的 max_length。
默认255
    
    
#### SOCIAL_LOGIN_CALLBACK_URL_PATTERN

用户认证结束后的回调地址，必须与 在OAuth2服务认证时提供的 redirect_uri 相匹配

默认设置为 `r'account/oauth/(?P<sitename>\w+)/?$'`

对应的 SOCIALOAUTH_SITES 设置见 [doc.md][1]


#### SOCIAL_LOGIN_DONE_REDIRECT_URL

用户认证成功后的跳转地址。默认为 '/'

如果用户是第一次登录，那么会为其分配一个新的内部uid，
如果以前已经登录过了，就获取其内部uid，然后将次uid设置到 session 中。
最后跳转到 `SOCIAL_LOGIN_DONE_REDIRECT_URL`
    
    
#### SOCIAL_LOGIN_SITEUSER_SELECT_RELATED

一个siteuser对象有三个 关联关系，（三个关联表）

*   inner_user  - 网站自身注册用户
*   social_user - 第三方帐号
*   user_info   - 用户信息

所以你可以通过 `request.siteuser.inner_user`, `request.siteuser.social_user`,
`request.siteuser.user_info` 来访问相应的数据。

这个就是配置 request.siteuser 在获取的时候，关联join哪几个表，
默认是 `user_info`， 因为获取用户信息是很频繁的操作。

你可以这样自定义: `SOCIAL_LOGIN_SITEUSER_SELECT_RELATED = ('user_info', 'social_user', 'inner_user')`

    
#### SOCIAL_LOGIN_ENABLE_ADMIN

是否开启 social_login 的admin。默认为开启。开启后的界面如下图：

![admin][4]
    
    
[1]: https://github.com/yueyoum/social-oauth/blob/master/doc.md#-settingspy
[2]: http://i1297.photobucket.com/albums/ag23/yueyoum/2_zpscfb21331.png
[3]: http://i1297.photobucket.com/albums/ag23/yueyoum/3_zps4c5735ae.png
[4]: http://i1297.photobucket.com/albums/ag23/yueyoum/4_zpsd0c7d263.png