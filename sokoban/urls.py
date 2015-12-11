from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapsViewSet, WallViewSet, BoxViewSet, PointViewSet, MenViewSet
from sk_auth.api.auth import RegisterView, LoginAPIView
from sk_game.api.game import GameViewSet

action_pk = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
action_no_pk = {'get': 'list', 'post': 'create'}

router = DefaultRouter()
router.register(r'maps', MapsViewSet)
router.register(r'auth/register', RegisterView)
urlpatterns = router.urls

urlpatterns_game = patterns('sk_game.api.game',
    url('^game/(?P<map>\d+)/$', GameViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    url('^game/$', GameViewSet.as_view(action_no_pk)),
)

urlpatterns_map_obj = patterns('sk_map.api.map',
    url('^wall/(?P<pk>\d+)/$', WallViewSet.as_view(action_pk)),
    url('^wall/$', WallViewSet.as_view(action_no_pk)),
    url('^box/(?P<pk>\d+)/$', BoxViewSet.as_view(action_pk)),
    url('^box/$', BoxViewSet.as_view(action_no_pk)),
    url('^point/(?P<pk>\d+)/$', PointViewSet.as_view(action_pk)),
    url('^point/$', PointViewSet.as_view(action_no_pk)),
    url('^men/(?P<pk>\d+)/$', MenViewSet.as_view(action_pk)),
    url('^men/$', MenViewSet.as_view(action_no_pk)),
)

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
urlpatterns += urlpatterns_map_obj
urlpatterns += urlpatterns_game
