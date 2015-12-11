from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from ..serializers.skins import SkinSerializer
from ..models import Skins


class SkinView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    A View for retrieve images for Game levels
    """
    serializer_class = SkinSerializer
    permission_classes = [AllowAny]
    queryset = Skins.objects.all()