from django.db import models
from sk_core.models import OwnableModel
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='media/')


class Skins(OwnableModel):

    box = models.ImageField(storage=fs, help_text='image url')
    point = models.ImageField(storage=fs, help_text='image url')
    men = models.ImageField(storage=fs, help_text='image url')
    wall = models.ImageField(storage=fs, help_text='image url')
    background = models.ImageField(storage=fs, help_text='image url')
