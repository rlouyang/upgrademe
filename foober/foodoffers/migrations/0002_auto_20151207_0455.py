# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import foodoffers.models


class Migration(migrations.Migration):

    dependencies = [
        ('foodoffers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodoffer',
            name='available_people',
            field=models.PositiveSmallIntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrequest',
            name='party_size',
            field=models.PositiveSmallIntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='prof_pic',
            field=models.ImageField(max_length=300, upload_to=foodoffers.models.rename_file),
        ),
    ]
