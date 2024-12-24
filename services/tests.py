from datetime import datetime

from django.test import TestCase
from django.core.management import call_command

from utils import test_data


class AgreementAdminTest(TestCase):
    """ Test custom features in admin/agreement """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        
        # Create Agreement
        self.agreement = test_data.create_agreement()
        
    def test_end_date(self):
        """ Valdate end_date format like dd/mo./yyyy """
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)
        
        # Open employee list page
        response = self.client.get("/admin/services/agreement/")
        
        # Validate date format
        self.assertContains(
            response,
            self.agreement.effective_date.strftime("%d/%b/%Y")
        )