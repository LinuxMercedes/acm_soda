from django.conf.urls.defaults import *

urlpatterns = patterns('acm_soda.web.views',
    ('^$', 'external'),
    ('profile/$', 'profile'),
    ('logout/$', 'profile_logout'),
)
