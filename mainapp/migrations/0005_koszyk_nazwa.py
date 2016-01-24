# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_atrakcja_miastoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='koszyk',
            name='nazwa',
            field=models.TextField(default='bleble'),
            preserve_default=False,
        ),
    ]
