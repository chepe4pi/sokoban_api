from django.db import models
from django_fsm import FSMField, transition

from sk_core.models import TimestampableModel, StatebleModel, OwnableModel, STATE_INITIAL, STATE_CHOICES, STATE_PRIVATE, \
    STATE_PUBLIC, STATE_DELETED, NotDeletedManager
from django.contrib.auth.models import User
from sk_skins.models import Skins


STATE_CHOICES_MAP = (
    (STATE_INITIAL, 'initial', 'Map'),
    (STATE_PUBLIC, 'ready / public', 'Map'),
    (STATE_PRIVATE, 'hidden / private', 'Map'),
    (STATE_DELETED, 'deleted', 'Map'),
)


class Map(OwnableModel, TimestampableModel):

    STATE_CHOICES = STATE_CHOICES_MAP

    title = models.CharField(max_length=255, help_text='title of map')
    players = models.ManyToManyField(
        User,
        through='sk_game.UserMapMembership',
        through_fields=('map', 'owner'),
        related_name='players'
    )
    skin = models.ForeignKey(Skins, default=1)
    rating = models.IntegerField(help_text="summary rating of map", null=True)
    state = FSMField(default=STATE_INITIAL, state_choices=STATE_CHOICES)

    objects = NotDeletedManager()

    @transition(field=state, source=STATE_PRIVATE, target=STATE_PUBLIC)
    def publish(self):
        pass

    @transition(field=state, source=STATE_PUBLIC, target=STATE_PRIVATE)
    def unpublish(self):
        pass

    @transition(field=state, source=STATE_DELETED, target='*')
    def block_change_state_deleted(self):
        raise NotImplementedError

    @transition(field=state, source=STATE_PUBLIC, target=STATE_DELETED)
    def block_delete_published(self):
        raise NotImplementedError


class MapLocation(StatebleModel, OwnableModel, TimestampableModel):

    x = models.PositiveSmallIntegerField(help_text='position by x coordinate')
    y = models.PositiveSmallIntegerField(help_text='position by y coordinate')

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.state), str(self.owner), '-', str(self.x), str(self.y)])


class OnMap(MapLocation):
    map = models.ForeignKey(Map, help_text='id of map that pointed')

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
