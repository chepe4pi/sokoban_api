from django.db import models
from django.contrib.auth.models import User

STATE_INITIAL = 0
STATE_PUBLIC = 1
STATE_PRIVATE = 2
STATE_DELETED = 3

STATE_CHOICES = (
    (STATE_INITIAL, 'initial'),
    (STATE_PUBLIC, 'ready / public'),
    (STATE_PRIVATE, 'hidden / private'),
    (STATE_DELETED, 'deleted'),
)


class NotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(state=STATE_DELETED)


class TimestampableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnableModel(models.Model):
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.owner)]) # TODO More ellegant way


class StatebleModel(models.Model):
    STATE_INITIAL = STATE_INITIAL
    STATE_PUBLIC = STATE_PUBLIC
    STATE_PRIVATE = STATE_PRIVATE
    STATE_DELETED = STATE_DELETED

    STATE_CHOICES = STATE_CHOICES

    objects = NotDeletedManager()

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES,
                                             default=STATE_INITIAL,
                                             help_text='status of object - initial / public / private / deleted')

    class Meta:
        abstract = True
