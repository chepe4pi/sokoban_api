from django.db import models
from sk_core.models import Timestampable
from django.contrib.auth.models import User


class MapLocation(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        setattr(self, 'x', x)
        setattr(self, 'y', y)
        self.save()

    class Meta:
        abstract = True


class Map(Timestampable):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)


class OnMap(models.Model):
    map = models.ForeignKey(Map)

    class Meta:
        abstract = True


class OnMapUniq(models.Model):
    map = models.ForeignKey(Map, unique=True)

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
