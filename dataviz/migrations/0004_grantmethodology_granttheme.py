# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataviz', '0003_methodology_sectorsubsector_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantMethodology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'n_grantmethodologytbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GrantTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'n_grantthemetbl',
                'managed': False,
            },
        ),
    ]
