from django.db import models
from sk_core.models import AccessibleModel, TimestampableModel


class Map(AccessibleModel, TimestampableModel):
    title = models.CharField(max_length=255)


class MapLocation(AccessibleModel, TimestampableModel):

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


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
