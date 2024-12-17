import os

from django.core.management.base import BaseCommand

from employees.models import WeeklyLoan

BASE_FILE = os.path.basename(__file__)


class Command(BaseCommand):
    help = 'Load data for all apps'
    
    def handle(self, *args, **kwargs):
        WeeklyLoan.objects.all().delete()