from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapsViewSet, MapDetailViewSet, WallViewSet, BoxViewSet, PointViewSet, MenViewSet
from sk_auth.api.auth import RegisterView


router = DefaultRouter()
router.register(r'maps', MapsViewSet)
router.register(r'map_details', MapDetailViewSet)
router.register(r'wall', WallViewSet)
router.register(r'box', BoxViewSet)
router.register(r'point', PointViewSet)
router.register(r'men', MenViewSet)
router.register(r'register', RegisterView)
urlpatterns = router.urls


urlpatterns_admin = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns_rest = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                            )

urlpatterns += urlpatterns_admin
urlpatterns += urlpatterns_rest