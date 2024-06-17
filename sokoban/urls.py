from django.urls import include, path, re_path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from sk_map.api.map import MapViewSet, WallViewSet, BoxViewSet, PointViewSet, MenViewSet, \
    WallListViewSet, BoxListViewSet, PointListViewSet, MenListViewSet, MapListViewSet
from sk_auth.api.auth import RegisterView, AuthAPIView
from sk_game.api.game import GameViewSet, orders_page_new
from sk_skins.api.skins import SkinView

action = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
action_with_patch = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}
action_no_pk = {'get': 'list', 'post': 'create'}
#
# router = DefaultRouter()
# router.register(r'skins', SkinView)
# router.register(r'auth/register', RegisterView)
# urlpatterns = router.urls

main_urls = [
    path('', orders_page_new),
]
#
# urlpatterns_game = [
#     re_path(r'^game/(?P<map>\d+)/$', GameViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
#     path('game/', GameViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
# ]
#
# urlpatterns_map = [
#     re_path(r'^map/(?P<pk>\d+)/$', MapViewSet.as_view(action_with_patch)),
#     path('map/', MapListViewSet.as_view(action_no_pk)),
# ]
#
# urlpatterns_map_obj = [
#     re_path(r'^wall/(?P<pk>\d+)/$', WallViewSet.as_view(action)),
#     path('wall/', WallListViewSet.as_view(action_no_pk)),
#     re_path(r'^box/(?P<pk>\d+)/$', BoxViewSet.as_view(action)),
#     path('box/', BoxListViewSet.as_view(action_no_pk)),
#     re_path(r'^point/(?P<pk>\d+)/$', PointViewSet.as_view(action)),
#     path('point/', PointListViewSet.as_view(action_no_pk)),
#     re_path(r'^men/(?P<pk>\d+)/$', MenViewSet.as_view(action)),
#     path('men/', MenListViewSet.as_view(action_no_pk)),
# ]
#
# urlpatterns_admin = [
#     path('admin/', admin.site.urls),
# ]
#
# urlpatterns_auth = [
#     path('auth/', AuthAPIView.as_view(), name='login_view'),
# ]

# patterns_swagger = [
#     path('docs/', include('rest_framework_swagger.urls')),
# ]

# urlpatterns += urlpatterns_admin
urlpatterns = main_urls
# urlpatterns += urlpatterns_auth
# urlpatterns += patterns_swagger
# urlpatterns += urlpatterns_map_obj
# urlpatterns += urlpatterns_game
# urlpatterns += urlpatterns_map
