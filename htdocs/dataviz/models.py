from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.timezone import utc

from django.db import models
from django.db.models import Q, Sum, Max

from django.contrib.auth.models import User

def validate_positive(value):
    if value <= 0:
        raise ValidationError('%s is not greater than zero' % value)


class Donor(models.Model):
    donor_id = models.PositiveIntegerField(db_column="DonorID", validators=[validate_positive,])
    name = models.CharField(db_column="Donor", max_length=3, null=True, blank=True)

    class Meta:
        managed = True
        db_table = "donortbl"
        ordering = ['name',]

    def __unicode__(self):
        return name

    def __str__(self):
        return name


class DonorDepartment(models.Model):
    department_id = models.PositiveIntegerField(db_column="DepartmentID", validators=[validate_positive,])
    donor = models.ForeignKey(Donor, db_column="DonorID")
    name = models.CharField(db_column="Department", max_length=255)

    class Meta:
        managed = True
        db_table = 'donordepttbl'
        ordering = ['name',]

    def __unicode__(self):
        return name

    def __str__(self):
        return name


class Region(models.Model):
    region_id = models.PositiveIntegerField(db_column="RegionID", validators=[validate_positive,])
    name = models.CharField(db_column="Region", max_length=100)
    
    class Meta:
        managed = True
        db_table = "regiontbl"
        ordering = ['name',]

    def __unicode__(self):
        return name

    def __str__(self):
        return name


class Country(models.Model):
    country_id = models.PositiveIntegerField(db_column="CountryID", validators=[validate_positive,])
    name = models.CharField(db_column="Country", max_length=100)
    region = models.ForeignKey(Region, db_column="RegionID", related_name="countries")
    iso2 = models.CharField(db_column="CountryCode", max_length="2")

    class Meta:
        managed = True
        db_table = "countrytbl"
        ordering = ['name',]

    def __unicode__(self):
        return name

    def __str__(self):
        return name



class Sector(models.Model):
    sector_id = models.PositiveIntegerField(db_column="SectorID", validators=[validate_positive,])
    name = models.CharField(db_column="Sector", max_length=100)

    class Meta:
        managed = True
        db_table = "n_sectortbl"
        ordering = ['name',]

    def __unicode__(self):
        return name

    def __str__(self):
        return name


class Grant(models.Model):
    grant_id = models.PositiveIntegerField(db_column="GrantID", validators=[validate_positive,])
    title = models.CharField(db_column="GrantTitle", max_length=250, null=True, blank=True)
    currency = models.CharField(db_column="Currency", max_length=3, null=True, blank=True)
    amount = models.DecimalField(db_column="Amount", max_digits=10, decimal_places=2, null=True, blank=True)
    amount_usd = models.DecimalField(db_column="USDAmount", max_digits=10, decimal_places=2)
    amount_icr = models.DecimalField(db_column="ICRAmount", max_digits=10, decimal_places=2)
    status = models.CharField(db_column="FundingStatus", max_length=50)
    hq_admin = models.CharField(db_column="HQadmin", max_length=3, null=True, blank=True)
    donor = models.ForeignKey(Donor, db_column="DonorID", related_name='grants')
    submission_date = models.DateField(db_column="SubmissionDate")
    start_date = models.DateField(db_column="StartDate")
    end_date = models.DateField(db_column="EndDate")
    rejected_date = models.DateField(db_column="RejectedDate")
    funding_probability = models.CharField(db_column="FundingProbability", max_length=255)
    complex_program = models.BooleanField(db_column="ComplexProgram")
    sensitive_data = models.BooleanField(db_column="SensitiveData")
    project_length = models.PositiveIntegerField(db_column="ProjectLength", validators=[validate_positive,])
    sectors = models.ManyToManyField(Sector, through="GrantSector")
    countries = models.ManyToManyField(Country, through="GrantCountry")

    def __unicode__(self):
        return title

    def __str__(self):
        return title

    class Meta:
        managed = True
        db_table = "granttbl"
        ordering = ['title',]

class GrantSector(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID")
    sector = models.ForeignKey(Sector, db_column="SectorID")

    class Meta:
        managed = True
        db_table = 'n_grantsectortbl'


class GrantCountry(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID")
    country = models.ForeignKey(Country, db_column="CountryID")

    class Meta:
        managed = True
        db_table = 'grantcountrytbl'



