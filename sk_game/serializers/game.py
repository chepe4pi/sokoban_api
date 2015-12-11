from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from sk_core.serializer import BaseModelSerializer
from sk_game.vallidators.solution import GameSolutionValidator
from sk_map.models import Map
from ..models import UserMapMembership


class GameSerializer(BaseModelSerializer):

    def validate_steps(self, value):
        solution = GameSolutionValidator(self.initial_data['map'], value)
        if solution.is_valid():
            return value
        else:
            raise ValidationError(_('Wrong solution'))

    def validate_rate(self, value):
        self.map = self._get_map_obj()
        if value is False or UserMapMembership.objects.filter(owner=self.context['request'].user,
                                                              map=self.map, done=True).count() > 0:
            return value
        else:
            raise ValidationError(_('First you have to took this map')) # TODO tests

    def validate_map(self, value):
        if Map.objects.filter(Q(public=True,
                                id=self.initial_data['map']) | Q(owner=self.context['request'].user.id,
                                                                 id=self.initial_data['map'])).count() > 0:
            return value
        else:
            raise ValidationError(_('This Map is not allowed')) # TODO tests

    def _get_map_obj(self):
        if 'map' not in self.initial_data:
            self.map = self.instance.map.id
        else:
            self.map = self.initial_data['map'] # TODO tests
        return self.map


    class Meta:
        model = UserMapMembership
        fields = ('rate', 'done', 'steps', 'map')
        extra_kwargs = {'steps': {'write_only': True}, 'done': {'read_only': True}}
