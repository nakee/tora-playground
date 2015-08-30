# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('full', models.CharField(max_length=500)),
                ('nikkud', models.CharField(max_length=500)),
                ('stripped', models.CharField(max_length=500)),
            ],
        ),

        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('start', models.ForeignKey(to='bible.Verse')),
            ],
        ),
    ]
