from django.test import TestCase
from django.core.management import call_command

from accounting import models
from utils import test_data


class CommandCreatePayrolls(TestCase):
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        employees_num = 2
        self.weekly_assistances = []
        for employee_num in range(employees_num):
            
            employee = test_data.create_employee(
                curp=f"CURP{employee_num}",
                ine=f"INE{employee_num}",
                phone=f"PHONE{employee_num}",
            )
            
            service = test_data.create_service(
                employee=employee,
            )
            
            weekly_assistance = test_data.create_weekly_assistance(
                service=service,
            )
            self.weekly_assistances.append(weekly_assistance)
            
    def test_run_with_weekly_assistance(self):
        """ Validate two create 2 payrolls """
        
        call_command("create_payrolls")
        
        # Validate payrolls created
        payrolls = models.Payroll.objects.all()
        self.assertEqual(payrolls.count(), 2)
        
        # Valdiate payroll data
        for weekly_assistance in self.weekly_assistances:
            payroll = models.Payroll.objects.filter(
                weekly_assistance=weekly_assistance
            )
            self.assertEqual(payroll.count(), 1)
            
    def test_run_without_weekly_assistance(self):
        """ Validate no payrolls created """
        
        # Delete weekly assistances
        for weekly_assistance in self.weekly_assistances:
            weekly_assistance.delete()
        
        call_command("create_payrolls")
        
        # Validate no payrolls created
        payrolls = models.Payroll.objects.all()
        self.assertEqual(payrolls.count(), 0)
        
            
            