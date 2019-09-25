# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataviz', '0002_donorcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Methodology',
            fields=[
                ('methodology_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'MethodologyID')),
                ('name', models.CharField(max_length=b'50', db_column=b'Methodology')),
            ],
            options={
                'db_table': 'n_methodologytbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SectorSubSector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'n_sectorsubsectortbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('theme_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'ThemeID')),
                ('name', models.CharField(max_length=b'50', db_column=b'Theme')),
            ],
            options={
                'db_table': 'n_themetbl',
                'managed': False,
            },
        ),
    ]
