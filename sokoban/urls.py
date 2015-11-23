from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapsViewSet


router = DefaultRouter()
router.register(r'maps', MapsViewSet)
urlpatterns = router.urls


urlpatterns_admin = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns_auth = patterns('sk_auth.api.auth',
    url('^auth/login/$', 'login_api_view', name='auth-login'),
    url('^auth/logout/$', 'logout_api_view', name='auth-logout'),
)

urlpatterns += urlpatterns_admin
urlpatterns += urlpatterns_auth
