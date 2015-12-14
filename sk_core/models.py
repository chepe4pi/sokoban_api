from django.db import models
from django.contrib.auth.models import User


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


class AccessibleModel(OwnableModel):
    public = models.BooleanField(default=False, help_text='object show for everyone or only for owner')

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join([str(self.id), str(self.public), str(self.owner)]) # TODO More ellegant way
