from setuptools import setup

from social_login import VERSION

packages = [
    'social_login',
]

install_requires = [
    'socialoauth',
]


setup(
    name='django-social-login',
    version = VERSION,
    license = 'BSD',
    description = 'A Django APP for Social account login via OAuth2 Service',
    long_description = open('README.txt').read(),
    author = 'Wang Chao',
    author_email = 'yueyoum@gmail.com',
    url = 'https://github.com/yueyoum/django-social-login',
    keywords = 'social, oauth, oauth2, django, login',
    packages = packages,
    install_requires = install_requires,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

