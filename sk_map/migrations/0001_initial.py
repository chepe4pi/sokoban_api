# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Men',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('aggrigator', models.OneToOneField(to='sk_map.Map')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('aggrigator', models.ForeignKey(to='sk_map.Map')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('aggrigator', models.ForeignKey(to='sk_map.Map')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='box',
            name='aggrigator',
            field=models.ForeignKey(to='sk_map.Map'),
        ),
    ]
