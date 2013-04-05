# django-social-login


用第三方帐号登录网站

## Usage

1.  install

    ```
    pip install django-social-login
    ```
    
    
2.  settings.py

    有几项是必要的设置，必须在项目 settings.py 中设置好
    
    *   把 `social_login` 加入到 `INSTALLED_APPS` 中
    
    *   SOCIALOAUTH_SITES
        
        要使用的提供OAuth2服务的站点信息，见 [socialoauth文档][1]
    
    *   SOCIAL_LOGIN_USER_INFO_MODEL
    
        用户信息的model，例如你的app名叫 myapp， 存储用户信息的model叫 UserInfo,
        那么这里就设置为 SOCIAL_LOGIN_USER_INFO_MODEL='myapp.UserInfo'
        
        UserInfo表中必须包含两个Field:
            username = models.CharField(max_length=32)
            avatar = models.CharField(max_length=255)
            
        用于存储第三方认证用户的用户名和头像url
        
        ### note
        username 不能设置 unique=True，因为不同网站用户的用户名可能相同
        
    *   SOCIAL_LOGIN_ERROR_REDIRECT_URL
    
        在用户认证过程中发生错误（用户拒绝授权等）时要跳转到的url
        
        
        
    *   'social_login.context_processors.social_sites'
    
        把它加入到 TEMPLATE_CONTEXT_PROCESSORS 中，
        并且在 views 中传递了 context_instance，
        那么在模板中就可以通过 `{% for s in social_sites %}` 的形式在获得配置的站点信息
        
            s.site_id       在 SOCIALOAUTH_SITES 中配置的 site_id
            s.site_name     站点的 英文名字
            s.site_name_zh  中文名字
            s.authorize_url 引导用户授权的url
        
        
    *   'social_login.middleware.SocialLoginUser'
    
        把它加入到 MIDDLEWARE_CLASSES 中，
        这样在每个 view 的 request 对象会有一个 siteuser 属性
        
        可以通过 `if request.siteuser` 来判断是否有用户登录。
        如果有 那么 request.siteuser 是一个 `social_login.SiteUser` 对象
        
        可以通过一下方法访问其属性：
        
            request.siteuser.id                 用户uid
            request.siteuser.is_social          是否是第三方帐号
            request.siteuser.date_joined        用户加入时间
            request.siteuser.info               用户信息对象
            request.siteuser.info_list(*args)   获取指定field的用户信息
        
        
        
3.  Other settings

    *   在你存储用户 登录/认证 信息的表中 设置 objects
        
        例子：
            from social_login.manager import InnerUserManager
            class UserAuth(models.Model):
                email = models.EmailField(unique=True)
                password = models.CharField(max_length=64)
                
                objects = InnerUserManager()
                
                
    
4.  runserver

    经过上面的设置后， `python manage.py validate` 无错误就 `python manage.py runserver`.
    如果有错，请确保正确安装，并且正确设置
    
    
## Login process

第三方登录和自己网站内部注册/登录的流程如下：

1.  当用户点击login后，提供两个选择：
    
    *   使用已经注册的帐号登录
    *   使用第三方帐号登录
    
    ![login][2]
    
2.  用户可以先 注册 ，并且用此帐号登录，也可以用第三方帐号登录。
    登录一些用户后的状态如下图：
    
    现在显示了登录过的用户信息，注意 uid为 5 和 6 的用户，
    他们来自不同的网站，但用户名却相同。
    所以在上面的设置中 username 不能设置为 unique=True
    
    ![status][3]
    

    
    
[1]: https://github.com/yueyoum/social-oauth
[2]: http://i1297.photobucket.com/albums/ag23/yueyoum/2_zpscfb21331.png
[3]: http://i1297.photobucket.com/albums/ag23/yueyoum/3_zps4c5735ae.png
