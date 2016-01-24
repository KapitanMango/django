# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_koszyk_nazwa'),
    ]

    operations = [
        migrations.AddField(
            model_name='miasta',
            name='wspolrzedne',
            field=models.ForeignKey(default='0', to='mainapp.Wspolrzedne'),
            preserve_default=False,
        ),
    ]
