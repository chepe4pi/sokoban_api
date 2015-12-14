from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapViewSet, WallViewSet, BoxViewSet, PointViewSet, MenViewSet,\
    WallListViewSet, BoxListViewSet, PointListViewSet, MenListViewSet, MapListViewSet
from sk_auth.api.auth import RegisterView, AuthAPIView
from sk_game.api.game import GameViewSet
from sk_skins.api.skins import SkinView


action = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
action_with_patch = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}
action_no_pk = {'get': 'list', 'post': 'create'}

router = DefaultRouter()
router.register(r'skins', SkinView)
router.register(r'auth/register', RegisterView)
urlpatterns = router.urls

urlpatterns_game = [
    url('^game/(?P<map>\d+)/$', GameViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    url('^game/$', GameViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
]

urlpatterns_map = {
    url('^map/(?P<pk>\d+)/$', MapViewSet.as_view(action_with_patch)),
    url('^map/$', MapListViewSet.as_view(action_no_pk)),
}

urlpatterns_map_obj = [
    url('^wall/(?P<pk>\d+)/$', WallViewSet.as_view(action)),
    url('^wall/$', WallListViewSet.as_view(action_no_pk)),
    url('^box/(?P<pk>\d+)/$', BoxViewSet.as_view(action)),
    url('^box/$', BoxListViewSet.as_view(action_no_pk)),
    url('^point/(?P<pk>\d+)/$', PointViewSet.as_view(action)),
    url('^point/$', PointListViewSet.as_view(action_no_pk)),
    url('^men/(?P<pk>\d+)/$', MenViewSet.as_view(action)),
    url('^men/$', MenListViewSet.as_view(action_no_pk)),
]

urlpatterns_admin =[
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns_auth = [
    url(r'^auth/', AuthAPIView.as_view(), name='login_view')
                            ]

patterns_swagger = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

urlpatterns += urlpatterns_admin
urlpatterns += urlpatterns_auth
urlpatterns += patterns_swagger
urlpatterns += urlpatterns_map_obj
urlpatterns += urlpatterns_game
urlpatterns += urlpatterns_map