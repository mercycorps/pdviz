# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dataviz.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'CountryID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=100, db_column=b'Country')),
                ('iso2', models.CharField(max_length=b'2', db_column=b'CountryCode')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'countrytbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('donor_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'DonorID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=3, null=True, db_column=b'Donor')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'donortbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DonorDepartment',
            fields=[
                ('department_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'DepartmentID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=255, db_column=b'Department')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'donordepttbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('grant_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'GrantID', validators=[dataviz.models.validate_positive])),
                ('title', models.CharField(max_length=250, null=True, db_column=b'GrantTitle')),
                ('currency', models.CharField(max_length=3, null=True, db_column=b'Currency')),
                ('amount', models.DecimalField(null=True, decimal_places=4, max_digits=20, db_column=b'Amount')),
                ('amount_usd', models.DecimalField(null=True, decimal_places=4, max_digits=20, db_column=b'USDAmount')),
                ('amount_icr', models.DecimalField(null=True, decimal_places=4, max_digits=20, db_column=b'ICRAmount')),
                ('status', models.CharField(max_length=50, null=True, db_column=b'FundingStatus')),
                ('hq_admin', models.CharField(max_length=3, null=True, db_column=b'HQadmin')),
                ('submission_date', models.DateField(null=True, db_column=b'SubmissionDate')),
                ('start_date', models.DateField(null=True, db_column=b'StartDate')),
                ('end_date', models.DateField(null=True, db_column=b'EndDate')),
                ('rejected_date', models.DateField(null=True, db_column=b'RejectedDate')),
                ('funding_probability', models.CharField(max_length=255, null=True, db_column=b'FundingProbability')),
                ('complex_program', models.BooleanField(db_column=b'ComplexProgram')),
                ('sensitive_data', models.BooleanField(db_column=b'SensitiveData')),
                ('project_length', models.PositiveIntegerField(null=True, db_column=b'ProjectLength', validators=[dataviz.models.validate_positive])),
                ('created', models.DateField(null=True, db_column=b'CreationDate')),
                ('updated', models.DateField(null=True, db_column=b'LastModifiedDate')),
            ],
            options={
                'db_table': 'granttbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GrantCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'grantcountrytbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GrantSector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'n_grantsectortbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'RegionID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=100, db_column=b'Region')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'regiontbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('sector_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'SectorID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=100, db_column=b'Sector')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'n_sectortbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SectorType',
            fields=[
                ('sector_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'SectorTypeID', validators=[dataviz.models.validate_positive])),
                ('sector_type', models.CharField(max_length=b'50', db_column=b'SectorType')),
            ],
            options={
                'db_table': 'n_sectortypetbl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubSector',
            fields=[
                ('subsector_id', models.PositiveIntegerField(serialize=False, primary_key=True, db_column=b'SubSectorID', validators=[dataviz.models.validate_positive])),
                ('name', models.CharField(max_length=b'50', db_column=b'SubSector')),
            ],
            options={
                'db_table': 'n_subsectortbl',
                'managed': False,
            },
        ),
    ]
