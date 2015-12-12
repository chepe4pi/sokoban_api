from sk_core.filters.backends import IsOwnerFilterBackend
from sk_core.views import BaseModelViewSet
from rest_framework.viewsets import ModelViewSet
from ..models import UserMapMembership
from rest_framework.permissions import IsAuthenticated
from ..serializers.game import GameSerializer
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class GameViewSet(BaseModelViewSet, ModelViewSet):
    """
    A ViewSet for Game objects
    """
    queryset = UserMapMembership.objects.all().select_related('map')
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    lookup_field = 'map'

    def perform_create(self, serializer):
        if UserMapMembership.objects.filter(map=serializer.validated_data['map'], owner=self.request.user).count() > 0:
            raise ValidationError({'non_field_errors': _('This Map User Membership already exist')})
        super(GameViewSet, self).perform_create(serializer)
        instance = serializer.save()
        setattr(instance, 'done', True)
        instance.save()

    class Meta:
        model = UserMapMembership
