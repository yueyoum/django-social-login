# -*- coding: utf-8 -*-

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class

from .utils import LazyList

def social_sites(request):
    def _social_sites():
        def make_site(s):
            s = import_oauth_class(s)()
            return {
                'site_id': s.site_id,
                'site_name': s.site_name,
                'site_name_zh': s.site_name_zh,
                'authorize_url': s.authorize_url,
            }
        return [make_site(s) for s in socialsites.list_sites()]
    
    return {'social_sites': LazyList(_social_sites)}
