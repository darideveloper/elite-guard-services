from django.test import TestCase
from django.core.management import call_command

from utils import test_data
from assistance import models


class AssistanceTest(TestCase):
    """ Test custom methods in assistance model """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        
        # Create initial data
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )
        self.week_days = [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday'
        ]
        
    def test_save_update_weekly_date_status(self):
        """ Validate day status updated in weekly assistance
        when change assistance status """
        
        # Update assistance status
        self.assistance.attendance = True
        self.assistance.save()
        week_day = self.assistance.date.weekday()
        
        # Valdiate weekly assistance status
        self.weekly_assistance.refresh_from_db()
        self.assertTrue(getattr(
            self.weekly_assistance,
            self.week_days[week_day]
        ))
        

class WeeklyAssistanceAdminTest(TestCase):
    """ Test custom features in admin/weekly-assistance """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        
        # Create WeeklyAssistance
        self.employee = test_data.create_employee()
        self.agreement = test_data.create_agreement()
        self.service = test_data.create_service(self.agreement, self.employee)
        self.weekly_assistance = models.WeeklyAssistance.objects.create(
            service=self.service,
        )
        
    def test_company_name(self):
        """ Validate company name in lst view """
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)
        
        # Open employee list page
        response = self.client.get("/admin/assistance/weeklyassistance/")
        
        # Validate company name
        self.assertContains(
            response,
            self.agreement.company_name,
        )
        
    def test_employee(self):
        """ Validate employee name in lst view """
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)
        
        # Open employee list page
        response = self.client.get("/admin/assistance/weeklyassistance/")
        
        # Validate company name
        self.assertContains(
            response,
            str(self.employee),
        )
        
        