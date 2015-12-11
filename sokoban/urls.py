from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapsViewSet, WallViewSet, BoxViewSet, PointViewSet, MenViewSet
from sk_auth.api.auth import RegisterView, LoginAPIView
from sk_game.api.game import GameViewSet


router = DefaultRouter()
router.register(r'maps', MapsViewSet)
router.register(r'wall', WallViewSet)
router.register(r'box', BoxViewSet)
router.register(r'point', PointViewSet)
router.register(r'men', MenViewSet)
router.register(r'game', GameViewSet)
router.register(r'auth/register', RegisterView)
urlpatterns = router.urls


urlpatterns_admin = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns_rest = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                            )

urlpatterns_auth = patterns('',
    url(r'^auth/login/', LoginAPIView.as_view(), name='login_view')
                            )

patterns_swagger = patterns('',
    url(r'^docs_sw/', include('rest_framework_swagger.urls')),
)

urlpatterns += urlpatterns_admin
urlpatterns += urlpatterns_rest
urlpatterns += urlpatterns_auth
urlpatterns += patterns_swagger
