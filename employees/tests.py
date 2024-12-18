from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from employees import models


class EmployeeModelTest(TestCase):
    """ Test custom methods in Employee Model"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")

        # Create an employee
        marital_status = models.MaritalStatus.objects.get(name="Soltero")
        education = models.Education.objects.get(name="Primaria")
        languages_es = models.Language.objects.get(name="Español")
        municipality = models.Municipality.objects.create(
            name="Estado / Municipio"
        )
        neighborhood = models.Neighborhood.objects.create(
            name="Neighborhood"
        )
        self.employee = models.Employee.objects.create(
            name="John",
            last_name_1="Doe",
            height=1.70,
            weight=70,
            marital_status=marital_status,
            education=education,
            birthdate="1990-01-01",
            municipality_birth=municipality,
            daily_rate=100,
            curp="CURP",
            ine="INE",
            knowledge="Knowledge",
            skills="Skills",
            municipality=municipality,
            neighborhood=neighborhood,
            postal_code="12345",
            address_street="Street",
            address_number="123",
            phone="1234567890",
            emergency_phone="0987654321",
        )
        self.employee.languages.add(languages_es)
        self.employee.save()
        
    def test_save_initial_status(self):
        """ Test set initial value in status_history """
        
        self.assertIn("Estado: Activo", self.employee.status_history)
        
    def test_save_new_status(self):
        """ Test set new value in status_history
        when status is updated """
        
        estatus_dismissed = models.Status.objects.get(name="Despido")
        self.employee.status = estatus_dismissed
        self.employee.save()
        
        self.assertIn("Estado: Activo >>> Despido", self.employee.status_history)
        
    def test_save_new_status_details(self):
        """ Test set new value in status_history
        when status is updated, with details """
        
        estatus_dismissed = models.Status.objects.get(name="Despido")
        details = "Por falta de asistencia"
        self.employee.status = estatus_dismissed
        self.employee.status_change_details = details
        self.employee.save()
        
        self.assertIn(
            f"Estado: Activo >>> Despido - Detalles: {details}",
            self.employee.status_history
        )
        
    def test_get_age_already_birthday(self):
        """ Test get age when birthday is 20 years ago on
        january 1st """
        
        # Set birthdate to 20 years ago
        current_year = timezone.now().year
        years = 20
        birthdate = timezone.datetime(current_year - years, 1, 1)
        self.employee.birthdate = birthdate
        self.employee.save()
        
        self.assertEqual(20, self.employee.get_age())
        
    def test_get_age_no_birthday_yet(self):
        """ Test get age when birthday is in 1 month """
        
        # set birthdate to 1 month from now
        current_year = timezone.now().year
        current_month = timezone.now().month
        next_month = current_month + 1
        if next_month == 13:
            next_month = 1
            current_year += 1
        years = 20
        birthdate = timezone.datetime(current_year - years, next_month, 1)
        self.employee.birthdate = birthdate
        self.employee.save()
        
        self.assertEqual(19, self.employee.get_age())
        

class LoanModelTest(TestCase):
    """ Test custom methods in Loan Model """
    
    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")

        # Create an employee
        marital_status = models.MaritalStatus.objects.get(name="Soltero")
        education = models.Education.objects.get(name="Primaria")
        languages_es = models.Language.objects.get(name="Español")
        municipality = models.Municipality.objects.create(
            name="Estado / Municipio"
        )
        neighborhood = models.Neighborhood.objects.create(
            name="Neighborhood"
        )
        self.employee = models.Employee.objects.create(
            name="John",
            last_name_1="Doe",
            height=1.70,
            weight=70,
            marital_status=marital_status,
            education=education,
            birthdate="1990-01-01",
            municipality_birth=municipality,
            daily_rate=100,
            curp="CURP",
            ine="INE",
            knowledge="Knowledge",
            skills="Skills",
            municipality=municipality,
            neighborhood=neighborhood,
            postal_code="12345",
            address_street="Street",
            address_number="123",
            phone="1234567890",
            emergency_phone="0987654321",
        )
        self.employee.languages.add(languages_es)
        self.employee.save()
        
    def test_save_update_balance_positive(self):
        """ Update employee balance when add a positive loan """
        
        models.Loan.objects.create(
            employee=self.employee,
            amount=100,
        )
        
        self.assertEqual(100, self.employee.balance)
        
    def test_save_update_balance_negative(self):
        """ Update employee balance when add a negative loan """
        
        models.Loan.objects.create(
            employee=self.employee,
            amount=-100,
        )
        
        self.assertEqual(-100, self.employee.balance)
        
        
        
        
