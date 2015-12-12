from django.db import models
from sk_core.models import OwnableModel
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='media/')


class Skins(OwnableModel):

    box = models.ImageField(storage=fs)
    point = models.ImageField(storage=fs)
    men = models.ImageField(storage=fs)
    wall = models.ImageField(storage=fs)
    background = models.ImageField(storage=fs)
