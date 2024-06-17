from django.db import models

from sk_core.models import OwnableModel, TimestampableModel
from sk_map.models import Map
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import JSONField


class UserMapMembership(OwnableModel, TimestampableModel):
    map = models.ForeignKey(Map, help_text='id of map that pointed to the game',on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(1)],
        null=True,
        blank=True,
        help_text="anyone can rate the public map, but only if it's done"
    )
    done = models.BooleanField(default=False, help_text='read_only field, will automatically set as True,'
                                                        ' if server receive correct solution from steps field')
    steps = JSONField(null=True, blank=True, help_text='level solution, sent to server after game level was done,'
                                                       ' format: [{x: 1, y: 2}, {x: 3, y: 4}, etc]')

    class Meta:
        unique_together = ('owner', 'map')
