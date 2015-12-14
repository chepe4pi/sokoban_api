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
    A ViewSet for Game objects, which created when User start to play the Map.
    """
    queryset = UserMapMembership.objects.all().select_related('map')
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    lookup_field = 'map'

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'patch':
            return super(GameViewSet, self).get_serializer(fields=('rate', 'done', 'steps'), *args, **kwargs)
        else:
            return super(GameViewSet, self).get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):

        """
        This method return a list and info about Game levels which user played.
        """
        return super(GameViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        This method return info about single Game level
        """
        return super(GameViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        This method create the Game when User start to play the Map.
        """
        return super(GameViewSet, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        This method set info about the Game (send solution steps or rate the Map, etc)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_create(self, serializer):
        if UserMapMembership.objects.filter(map=serializer.validated_data['map'], owner=self.request.user).count() > 0:
            raise ValidationError({'non_field_errors': _('This Map User Membership already exist')})
        super(GameViewSet, self).perform_create(serializer)
        instance = serializer.save()
        setattr(instance, 'done', True)
        instance.save()

    class Meta:
        model = UserMapMembership
