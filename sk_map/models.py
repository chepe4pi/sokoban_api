from django.db import models
from sk_core.models import AccessibleModel, TimestampableModel
from django.contrib.auth.models import User


class Map(AccessibleModel, TimestampableModel):
    title = models.CharField(max_length=255)
    players = models.ManyToManyField(
        User,
        through='sk_game.UserMapMembership',
        through_fields=('map', 'owner'),
        related_name='players'
    )


class MapLocation(AccessibleModel, TimestampableModel):

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.public), str(self.owner), '-', str(self.x), str(self.y)])

class OnMap(MapLocation):
    map = models.ForeignKey(Map)

    class Meta:
        abstract = True
        unique_together = ("x", "y", "map")


class OnMapUniq(MapLocation):
    map = models.OneToOneField(Map)

    class Meta:
        abstract = True


class Box(OnMap):
    pass


class Point(OnMap):
    pass


class Wall(OnMap):
    pass


class Men(OnMapUniq):
    pass
