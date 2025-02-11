from django.core.management.base import BaseCommand
from django.utils import timezone

from assistance.models import Assistance, WeeklyAssistance
from services import models as services_models
from utils.dates import get_current_week


class Command(BaseCommand):
    help = 'Create a daily assistance for each service'
    
    def handle(self, *args, **options):
        
        services = services_models.Service.objects.all()
        
        for service in services:
            
            print(f"Service: {service}")
            
            # Get or create weekly assistance
            week_number = get_current_week()
            weekly_assistance = WeeklyAssistance.objects.get(
                service=service,
                week_number=week_number,
            )
            
            today = timezone.now().date()
            assistance = Assistance.objects.filter(
                date=today,
                weekly_assistance=weekly_assistance
            )
            if assistance:
                # Skip this service
                print("\tAssistance already exists")
            else:
                # Create new asistance for today
                assistance = Assistance.objects.create(
                    attendance=False,
                    weekly_assistance=weekly_assistance
                )
                assistance.save()
                print("\tCreated assistance")