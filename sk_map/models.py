from django.db import models
from sk_core.models import AccessibleModel, TimestampableModel


class Map(AccessibleModel, TimestampableModel):
    title = models.CharField(max_length=255)
    x_size = models.PositiveSmallIntegerField()
    y_size = models.PositiveSmallIntegerField()


class MapLocation(AccessibleModel, TimestampableModel):

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        app_label = 'sk_map' # TODO add app label


class OnMap(MapLocation):
    map = models.ForeignKey(Map)

    class Meta:
        abstract = True


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
