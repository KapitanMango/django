# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_koszyk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Miasta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miasto', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='atrakcja',
            name='miasto',
            field=models.ForeignKey(to='mainapp.Miasta'),
        ),
    ]
