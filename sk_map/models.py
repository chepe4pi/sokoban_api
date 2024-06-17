from django.db import models
from sk_core.models import AccessibleModel, TimestampableModel
from django.contrib.auth.models import User
from sk_skins.models import Skins


class Map(AccessibleModel, TimestampableModel):
    title = models.CharField(max_length=255, help_text='title of map')
    players = models.ManyToManyField(
        User,
        through='sk_game.UserMapMembership',
        through_fields=('map', 'owner'),
        related_name='players'
    )
    skin = models.ForeignKey(Skins, default=1, on_delete=models.CASCADE)
    rating = models.IntegerField(help_text="summary rating of map", null=True)


class MapLocation(AccessibleModel, TimestampableModel):

    x = models.PositiveSmallIntegerField(help_text='position by x coordinate')
    y = models.PositiveSmallIntegerField(help_text='position by y coordinate')

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.public), str(self.owner), '-', str(self.x), str(self.y)])


class OnMap(MapLocation):
    map = models.ForeignKey(Map, help_text='id of map that pointed', on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ("x", "y", "map")


class OnMapUniq(MapLocation):
    map = models.OneToOneField(Map,on_delete=models.CASCADE)

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
