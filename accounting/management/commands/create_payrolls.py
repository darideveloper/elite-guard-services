from django.core.management.base import BaseCommand
from django.utils import timezone

from assistance import models as assistance_models
from accounting import models as accounting_models
from employees import models as employees_models


class Command(BaseCommand):
    help = 'Create a payroll for each wmployee / weekly asistance'
    
    def handle(self, *args, **options):
        
        # Get last week of the year
        year = timezone.now().year
        last_weekly_assistance = assistance_models.WeeklyAssistance.objects.filter(
            start_date__year=year
        ).order_by('week_number').last()
        
        # End if no weekly assistances
        if last_weekly_assistance is None:
            print("No weekly assistances found")
            return
        
        last_week_number = last_weekly_assistance.week_number
        print(f"Last week of the year: {last_week_number}")
        
        # Get weekly assistances of the last week
        weekly_assistances = assistance_models.WeeklyAssistance.objects.filter(
            week_number=last_week_number
        )
        print(f"Found {weekly_assistances.count()} weekly assistances")
        
        # Create each payroll
        for weekly_assistance in weekly_assistances:
            
            employee = weekly_assistance.service.employee
            employee_loans = employees_models.Loan.objects.filter(
                employee=employee,
                amount__lt=0
            )
            loans_total = sum([loan.amount for loan in employee_loans])
            
            # Skip payroll if already exists
            if accounting_models.Payroll.objects.filter(
                weekly_assistance=weekly_assistance
            ).exists():
                print(f"Payroll for {employee} already exists")
                continue
            
            # Create new payroll
            accounting_models.Payroll.objects.create(
                weekly_assistance=weekly_assistance,
                discount_loans=loans_total
            )
            print(f"Created payroll for {employee}")