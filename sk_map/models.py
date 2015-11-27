from django.db import models
from sk_core.models import Timestampable
from django.contrib.auth.models import User


class Map(Timestampable):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User)

    def get_owner(self):
        return self.owner

    def is_public(self):
        return self.public

    def __str__(self):
        return ' '.join([str(self.id), str(self.public), str(self.owner)]) # TODO global method defenition


class MapLocation(Timestampable, models.Model):

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def get_owner(self):
        return self.aggrigator.owner

    def is_public(self):
        return self.aggrigator.public

    class Meta:
        abstract = True


class OnMap(MapLocation):
    aggrigator = models.ForeignKey(Map)

    class Meta:
        abstract = True


class OnMapUniq(MapLocation):
    aggrigator = models.OneToOneField(Map)

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
