from django.db import models
from django.contrib.auth.models import User


class TimestampableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccessibleModel(models.Model):
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.public), str(self.owner)]) # TODO More ellegant way
