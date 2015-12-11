from django.db import models
from sk_core.models import OwnableModel, TimestampableModel
from sk_map.models import Map
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserMapMembership(OwnableModel, TimestampableModel):
    map = models.ForeignKey(Map)
    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(1)],
        null=True,
        blank=True
    )
    done = models.BooleanField(default=False)
    steps = JSONField()

    class Meta:
        unique_together = ('owner', 'map')
