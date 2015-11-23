import random
import datetime
import jwt
from django.conf import settings
from django.db import models
from sk_core.models import Timestampable


class AuthToken(Timestampable, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_token')
    token = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_token(self):
        return jwt.encode({
            'user_id': self.user_id,
            'rnd': random.random(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, settings.SECRET_KEY)

    def __unicode__(self):
        return self.token
