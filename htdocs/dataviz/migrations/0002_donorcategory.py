# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dataviz.models


class Migration(migrations.Migration):

    dependencies = [
        ('dataviz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorCategory',
            fields=[
                ('donor_category_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'DonorCategoryID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=255, db_column=b'DonorCategory')),
            ],
            options={
                'db_table': 'donorcategorytbl',
                'managed': False,
            },
        ),
    ]
