from django.db import models
from sk_core.models import Timestampable
from django.contrib.auth.models import User


class Map(Timestampable, models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=False)


class MapLocation(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def set_position(self, x, y):
        setattr(self, 'x', x)
        setattr(self, 'y', y)
        self.save()

    class Meta:
        abstract = True


class OnMap(models.Model):
    map = models.ForeignKey(Map)

    class Meta:
        abstract = True


class OnMapUniq(models.Model):
    map = models.OneToOneField(Map)

    class Meta:
        abstract = True


class Box(Timestampable, MapLocation, OnMap, models.Model):
    pass


class Point(Timestampable, MapLocation, OnMap, models.Model):
    pass


class Wall(Timestampable, MapLocation, OnMap, models.Model):
    pass


class Men(Timestampable, MapLocation, OnMapUniq, models.Model):
    pass
