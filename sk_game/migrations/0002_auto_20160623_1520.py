# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 15:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sk_map', '0001_initial'),
        ('sk_game', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usermapmembership',
            name='map',
            field=models.ForeignKey(help_text='id of map that pointed to the game', on_delete=django.db.models.deletion.CASCADE, to='sk_map.Map'),
        ),
        migrations.AddField(
            model_name='usermapmembership',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usermapmembership',
            unique_together=set([('owner', 'map')]),
        ),
    ]
