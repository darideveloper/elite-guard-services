from django.core.management.base import BaseCommand

from assistance import models as assistance_models
from services import models as services_models
from utils.dates import get_current_week


class Command(BaseCommand):
    help = 'Create a daily assistance for each service'
    
    def handle(self, *args, **options):
        services = services_models.Service.objects.all()
        
        for service in services:
            
            print(f"Service: {service}")
            
            weekly_assistance = assistance_models.WeeklyAssistance.objects.filter(
                service=service,
                week_number=get_current_week()
            )
            if weekly_assistance:
                # Skip week creation
                print("\tWeekly assistance already exists")
            else:
                # Create new weekly assistance
                weekly_assistance = assistance_models.WeeklyAssistance(
                    service=service,
                )
                weekly_assistance.save()
                print("\tCreated weekly assistance")