# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20160112_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='atrakcja',
            name='miastoto',
            field=models.TextField(default='Krakow'),
            preserve_default=False,
        ),
    ]
