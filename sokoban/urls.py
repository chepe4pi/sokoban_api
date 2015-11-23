from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns_admin = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns_auth = patterns('sk_auth.api.auth',
    url('^auth/login/$', 'login_api_view', name='auth-login'),
    url('^auth/logout/$', 'logout_api_view', name='auth-logout'),
)

urlpatterns_map = patterns('sk_map.api.map',
    url('^maps/$', 'maps_list_api_view', name='sk-map'),
    url('^map/(?P<pk>\d+)$', 'map_api_view', name='sk-map-urd'),
    url('^map/$', 'map_create_api_view', name='sk-map-c'),
#    url('^box/(?P<id>\d+)$', 'box_list_api_view', name='sk-box'),
#    url('^wall/(?P<id>\d+)$', 'wall_list_api_view', name='sk-wall'),
#    url('^men/(?P<id>\d+)$', 'men_list_api_view', name='sk-men'),
#    url('^point/(?P<id>\d+)$', 'point_list_api_view', name='sk-point'),
)

urlpatterns = patterns('',)
urlpatterns += urlpatterns_admin
urlpatterns += urlpatterns_auth
urlpatterns += urlpatterns_map
