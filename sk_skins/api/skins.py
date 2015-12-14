from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from ..serializers.skins import SkinSerializer
from ..models import Skins
from ..filters.map import SkinFilterSet


class SkinView(ListModelMixin, GenericViewSet):
    """
    A View for retrieve images for Game levels.
    Any Map can be pointed to any Skin. The fields bellow contain links to images.
    """
    serializer_class = SkinSerializer
    permission_classes = [AllowAny]
    queryset = Skins.objects.all()
    filter_class = SkinFilterSet
