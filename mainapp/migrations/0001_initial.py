# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ulica', models.TextField()),
                ('nr_budynku', models.IntegerField()),
                ('nr_domu', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Atrakcja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miasto', models.TextField()),
                ('typ', models.TextField()),
                ('nazwa', models.TextField()),
                ('czas_otwarcia', models.TimeField()),
                ('czas_zamkniecia', models.TimeField()),
                ('czas', models.FloatField()),
                ('cena', models.FloatField()),
                ('opis', models.TextField()),
                ('adres', models.ForeignKey(to='mainapp.Adres')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wspolrzedne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wsp_x', models.FloatField()),
                ('wsp_y', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='atrakcja',
            name='wspolrzedne',
            field=models.ForeignKey(to='mainapp.Wspolrzedne'),
            preserve_default=True,
        ),
    ]
