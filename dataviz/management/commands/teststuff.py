from django.core.management.base import BaseCommand, CommandError
from django.db.models import DecimalField, IntegerField, CharField, ExpressionWrapper, F, Case, Value, When, Q, Sum, Avg, Max, Min, Count
from dataviz.models import Region

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        regions = Region.objects.annotate(
            funded_usd=Sum(
                Case(
                    When(
                        Q(countries__grants__status='Closed')|
                        Q(countries__grants__status='Funded')|
                        Q(countries__grants__status='Completed'), then='countries__grants__amount_usd'
                    ),
                    output_field=IntegerField(),
                )
            )
        )
        for r in regions:
            print r.name, r.num_funded
