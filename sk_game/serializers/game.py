from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from sk_core.serializer import BaseModelSerializer
from sk_game.vallidators.solution import GameSolutionValidator
from sk_map.models import Map
from ..models import UserMapMembership


class GameSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(GameSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate_steps(self, value):
        solution = GameSolutionValidator(self.initial_data['map'], value)
        if solution.is_valid():
            return value
        else:
            raise ValidationError(_('Wrong solution'))

    def validate_rate(self, value):
        self.map = self._get_map_obj()
        try:
            membership = UserMapMembership.objects.get(owner=self.context['request'].user, map=self.map, done=True)
        except UserMapMembership.DoesNotExist:
            raise ValidationError(_('First you have to took this map'))  # TODO tests
        if not membership.rate:
            old_rating = self.instance.map.rating or 0
            new_rating = old_rating + value
            self.instance.map.rating = new_rating
            self.instance.map.save()

    def validate_map(self, value):
        if Map.objects.filter(Q(public=True,
                                id=self.initial_data['map']) | Q(owner=self.context['request'].user.id,
                                                                 id=self.initial_data['map'])).count() > 0:
            return value
        else:
            raise ValidationError(_('This Map is not allowed'))  # TODO tests

    def _get_map_obj(self):
        if 'map' not in self.initial_data:
            self.map = self.instance.map.id
        else:
            self.map = self.initial_data['map']  # TODO tests
        return self.map

    class Meta:
        model = UserMapMembership
        fields = ('rate', 'done', 'steps', 'map')
        extra_kwargs = {'steps': {'write_only': True}, 'done': {'read_only': True}}
