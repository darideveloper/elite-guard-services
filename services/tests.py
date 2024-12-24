from datetime import datetime

from django.test import TestCase
from django.core.management import call_command

from utils import test_data
from services import models


class AgreementAdminTest(TestCase):
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass = test_data.create_admin_user()
        
        # Create Agreement
        self.agreement = models.Agreement.objects.create(
            company_name="Company Test",
            salary=1000,
            responsible_name="Responsible Test",
            responsible_phone="1234567890",
            effective_date="2020-01-01",
        )
        
    def test_end_date(self):
        """ Valdate end_date format like dd/mo./yyyy """
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)
        
        # Open employee list page
        response = self.client.get("/admin/services/agreement/")
        
        # Validate date format
        date_str = self.agreement.effective_date
        date = datetime.strptime(date_str, "%Y-%m-%d")
        self.assertContains(
            response,
            date.strftime("%d/%b/%Y"),
        )