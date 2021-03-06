from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Count


class DBRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'dataviz':
            return 'gait'
        return None


def validate_positive(value):
    if value <= 0:
        raise ValidationError('%s is not greater than zero' % value)


class DonorCategory(models.Model):
    donor_category_id = models.PositiveIntegerField(
        primary_key=True, db_column="DonorCategoryID", validators=[validate_positive])
    name = models.CharField(db_column="DonorCategory", max_length=255)

    class Meta:
        managed = False
        db_table = 'donorcategorytbl'

    def __str__(self):
        return self.name


class Donor(models.Model):
    donor_id = models.PositiveIntegerField(primary_key=True, db_column="DonorID", validators=[validate_positive])
    name = models.CharField(db_column="Donor", max_length=3, null=True)
    category = models.ForeignKey(
        DonorCategory, db_column="DonorCategoryID", related_name="donors", on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "donortbl"
        ordering = ['name']

    @property
    def num_of_grants(self):
        return self.grants.aggregate(num_grants=Count('grant_id'))['num_grants']

    def __str__(self):
        return self.name or ''


class DonorDepartment(models.Model):
    department_id = models.PositiveIntegerField(
        primary_key=True, db_column="DepartmentID", validators=[validate_positive])
    donor = models.ForeignKey(Donor, db_column="DonorID", on_delete=models.CASCADE)
    name = models.CharField(db_column="Department", max_length=255)

    class Meta:
        managed = False
        db_table = 'donordepttbl'
        ordering = ['name']

    def __str__(self):
        return self.name or ''


class Region(models.Model):
    region_id = models.PositiveIntegerField(primary_key=True, db_column="RegionID", validators=[validate_positive])
    name = models.CharField(db_column="Region", max_length=100)

    class Meta:
        managed = False
        db_table = "regiontbl"
        ordering = ['name']

    def __str__(self):
        return self.name or ''


class Country(models.Model):
    country_id = models.PositiveIntegerField(primary_key=True, db_column="CountryID", validators=[validate_positive])
    name = models.CharField(db_column="Country", max_length=100)
    region = models.ForeignKey(Region, db_column="RegionID", related_name="countries", on_delete=models.CASCADE)
    iso2 = models.CharField(db_column="CountryCode", max_length=2)

    class Meta:
        managed = False
        db_table = "countrytbl"
        ordering = ['name']

    def __str__(self):
        return self.name or ''


class Sector(models.Model):
    sector_id = models.PositiveIntegerField(primary_key=True, db_column="SectorID", validators=[validate_positive])
    name = models.CharField(db_column="Sector", max_length=100)

    class Meta:
        managed = False
        db_table = "n_sectortbl"
        ordering = ['name']

    def __str__(self):
        return self.name or ''


class SubSector(models.Model):
    subsector_id = models.PositiveIntegerField(
        primary_key=True, db_column="SubSectorID", validators=[validate_positive])
    name = models.CharField(db_column="SubSector", max_length=50)
    sectors = models.ManyToManyField(Sector, through="SectorSubSector")

    class Meta:
        managed = False
        db_table = 'n_subsectortbl'

    def __str__(self):
        return self.name or ''


class SectorSubSector(models.Model):
    sector = models.ForeignKey(Sector, db_column="SectorID", on_delete=models.CASCADE)
    subsector = models.ForeignKey(SubSector, db_column="SubSectorID", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'n_sectorsubsectortbl'


class SectorType(models.Model):
    sector_id = models.PositiveIntegerField(primary_key=True, db_column="SectorTypeID", validators=[validate_positive])
    sector_type = models.CharField(db_column="SectorType", max_length=50)

    class Meta:
        managed = False
        db_table = "n_sectortypetbl"

    def __str__(self):
        return self.sector_type or ''


class Theme(models.Model):
    theme_id = models.PositiveIntegerField(primary_key=True, db_column='ThemeID')
    name = models.CharField(db_column="Theme", max_length=50)

    class Meta:
        managed = False
        db_table = 'n_themetbl'

    def __str__(self):
        return self.name or ''


class Methodology(models.Model):
    methodology_id = models.PositiveIntegerField(primary_key=True, db_column='MethodologyID')
    name = models.CharField(db_column='Methodology', max_length=50)

    class Meta:
        managed = False
        db_table = 'n_methodologytbl'

    def __str__(self):
        return self.name or ''


class GrantsWonManager(models.Manager):
    def get_queryset(self):
        return super(GrantsWonManager, self).get_queryset().filter(
            Q(status='Closed') |
            Q(status='Funded') |
            Q(status='Completed')
        )


class GrantsLostManager(models.Manager):
    def get_queryset(self):
        return super(GrantsLostManager, self).get_queryset().filter(
                Q(status="Rejected"))


class BothWonLostGrants(models.Manager):
    def get_queryset(self):
        return super(BothWonLostGrants, self).get_queryset().filter(
            Q(status='Closed') |
            Q(status='Funded') |
            Q(status='Completed') |
            Q(status="Rejected")
        )


class Grant(models.Model):
    grant_id = models.PositiveIntegerField(primary_key=True, db_column="GrantID", validators=[validate_positive])
    title = models.CharField(db_column="GrantTitle", max_length=250, null=True)
    currency = models.CharField(db_column="Currency", max_length=3, null=True)
    amount = models.DecimalField(db_column="Amount", max_digits=20, decimal_places=4, null=True)
    amount_usd = models.DecimalField(db_column="USDAmount", max_digits=20, decimal_places=4, null=True)
    amount_icr = models.DecimalField(db_column="ICRAmount", max_digits=20, decimal_places=4, null=True)
    status = models.CharField(db_column="FundingStatus", max_length=50, null=True)
    hq_admin = models.CharField(db_column="HQadmin", max_length=3, null=True)
    donor = models.ForeignKey(Donor, db_column="DonorID", related_name='grants', null=True, on_delete=models.PROTECT)
    submission_date = models.DateField(db_column="SubmissionDate", null=True)
    start_date = models.DateField(db_column="StartDate", null=True)
    end_date = models.DateField(db_column="EndDate", null=True)
    rejected_date = models.DateField(db_column="RejectedDate", null=True)
    funding_probability = models.CharField(db_column="FundingProbability", max_length=255, null=True)
    complex_program = models.BooleanField(db_column="ComplexProgram")
    sensitive_data = models.BooleanField(db_column="SensitiveData")
    project_length = models.PositiveIntegerField(db_column="ProjectLength", validators=[validate_positive], null=True)
    created = models.DateField(db_column="CreationDate", null=True)
    updated = models.DateField(db_column="LastModifiedDate", null=True)
    sectors = models.ManyToManyField(Sector, through="GrantSector")
    subsectors = models.ManyToManyField(SubSector, through='GrantSector')
    themes = models.ManyToManyField(Theme, through='GrantTheme')
    methodologies = models.ManyToManyField(Methodology, through='GrantMethodology')
    countries = models.ManyToManyField(Country, through="GrantCountry", related_name='grants')
    objects = models.Manager()
    won_grants = GrantsWonManager()
    lost_grants = GrantsLostManager()
    both_won_n_loss_grants = BothWonLostGrants()
    department = models.ForeignKey(
        DonorDepartment, db_column="DepartmentID", related_name='grants', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title or ''

    class Meta:
        managed = False
        db_table = "granttbl"


class GrantTheme(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID", on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, db_column="ThemeID", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'n_grantthemetbl'
        unique_together = (('grant', 'theme'),)


class GrantMethodology(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID", on_delete=models.CASCADE)
    methodology = models.ForeignKey(Methodology, db_column="MethodologyID", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "n_grantmethodologytbl"


class GrantSector(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID", on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, db_column="SectorID", on_delete=models.CASCADE)
    subsector = models.ForeignKey(SubSector, db_column="SubSectorID", null=True, on_delete=models.CASCADE)
    sector_type = models.ForeignKey(SectorType, db_column="SectorTypeID", null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'n_grantsectortbl'
        unique_together = (("grant", "sector", "subsector", "sector_type"),)


class GrantCountry(models.Model):
    grant = models.ForeignKey(Grant, db_column="GrantID", on_delete=models.CASCADE)
    country = models.ForeignKey(Country, db_column="CountryID", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'grantcountrytbl'
        unique_together = (("grant", "country"),)
