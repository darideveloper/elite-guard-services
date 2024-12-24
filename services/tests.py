from django.test import TestCase
from django.core.management import call_command

from utils import test_data


class AgreementModelTest(TestCase):
    """ Validate custom methods in model """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        
        # Create Agreement
        self.agreement = test_data.create_agreement()
        self.employee = test_data.create_employee()
        self.service = test_data.create_service(
            agreement=self.agreement,
            employee=self.employee
        )
        
    def test_get_services(self):
        """ Validate get_services method """
        
        # Get services
        services = self.agreement.get_services()
        
        # Validate services
        self.assertEqual(services.count(), 1)
        self.assertEqual(services[0], self.service)
        
    def test_get_employees(self):
        """ Validate get_employees method """
        
        # Get employees
        employees = self.agreement.get_employees()
        
        # Validate employees
        self.assertEqual(employees.count(), 1)
        self.assertEqual(employees[0], self.employee)
        

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