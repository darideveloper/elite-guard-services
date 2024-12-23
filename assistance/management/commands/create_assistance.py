from django.core.management.base import BaseCommand
from django.utils import timezone

from assistance import models as assistance_models
from services import models as services_models


class Command(BaseCommand):
    help = 'Create a daily assistance for each service'
    
    def handle(self, *args, **options):
        services = services_models.Service.objects.all()
        
        for service in services:
            
            print(f"Service: {service}")
            
            # Validate if the assistance already exists
            today = timezone.now().date()
            assistance = assistance_models.Assistance.objects.filter(
                service=service,
                date=today
            )
            if assistance:
                # Skip this service
                print("\tAssistance already exists")
            else:
                # Create new asistance for today
                assistance = assistance_models.Assistance(
                    service=service,
                    attendance=False,
                )
                assistance.save()
                print("\tCreated assistance")