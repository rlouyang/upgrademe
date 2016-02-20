# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('address', models.TextField(max_length=1000)),
                ('description', models.TextField(max_length=2000)),
                ('picture', models.ImageField(upload_to=b'/food/')),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('max_people', models.PositiveSmallIntegerField()),
                ('offer_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FoodRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('accepted', models.BooleanField(default=False)),
                ('offer', models.ForeignKey(to='foodoffers.FoodOffer')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10)),
                ('prof_pic', models.ImageField(upload_to=b'/profiles/')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='foodrequest',
            name='requester',
            field=models.ForeignKey(to='foodoffers.User'),
        ),
        migrations.AddField(
            model_name='foodoffer',
            name='user',
            field=models.ForeignKey(to='foodoffers.User'),
        ),
    ]
