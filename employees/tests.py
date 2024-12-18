from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from employees import models
from utils.test_data import create_employee, create_admin_user


class EmployeeModelTest(TestCase):
    """ Test custom methods in Employee Model"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.employee = create_employee()
        
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
        self.employee = create_employee()
        
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
        
        
class EmployeeAdminTest(TestCase):
    """ Test custom features in admin/employee """
    
    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.employee = create_employee()
        self.admin_user, self.admin_pass = create_admin_user()
        
    def test_actions_links(self):
        """ Validate custom action links """
        
        links = {
            "Imprimir": "/employees/report/employee-details/1",
            "Ver": "/employees/report/employee-preview/1",
        }
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)
        
        # Open employee list page
        response = self.client.get("/admin/employees/employee/")
        
        # Validate links
        for link_text, link in links.items():
            self.assertContains(response, link_text)
            self.assertContains(response, link)
            
            
class ReportEmployeeDetailsViewTest(TestCase):
    """ Test content of custom view with employee details """
    
    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.employee = create_employee()
        self.admin_user, self.admin_pass = create_admin_user()
        
        self.endpoint = f"/employees/report/employee-details/{self.employee.id}/"
    
    def test_unauthorized(self):
        """ Validate redirect when user is not logged in
        or don't have permission """
        
        # Open page
        response = self.client.get(self.endpoint)
        
        # Validate redirect
        self.assertEqual(302, response.status_code)
    
    def test_content(self):
        """ Valdiate content in page """
        
        # Create refs
        refs_numbers = ["1000000001", "1000000002"]
        for number in refs_numbers:
            models.Ref.objects.create(
                employee=self.employee,
                name="Ref",
                phone=number,
            )
            
        # Create relatives
        relatives = [
            {
                "name": "Relative 1",
                "last_name_1": "Last 1",
                "last_name_2": "Last 2",
                "relationship": "Padre",
                "phone": "1000000003",
                "age": 50,
            },
            {
                "name": "Relative 2",
                "last_name_1": "Last 3",
                "last_name_2": "Last 4",
                "relationship": "Madre",
                "phone": "1000000004",
                "age": 45,
            }
        ]
        for relative in relatives:
            relationship = models.Relationship.objects.get(name=relative["relationship"])
            models.Relative.objects.create(
                employee=self.employee,
                name=relative["name"],
                last_name_1=relative["last_name_1"],
                last_name_2=relative["last_name_2"],
                relationship=relationship,
                phone=relative["phone"],
                age=relative["age"],
            )
        
        # Employee details
        report_data = {
            "Fecha de ingreso": self.employee.created_at.strftime("%d/%m/%Y"),
            "No. de Empleado": f"EGS{self.employee.id}",
            "Apellido Paterno": self.employee.last_name_1,
            "Apellido Materno": self.employee.last_name_2,
            "Nombre(s)": self.employee.name,
            "Edad": self.employee.get_age(),
            "Estatura": self.employee.height,
            "Peso": self.employee.weight,
            "Estado Civil": self.employee.marital_status.name.upper(),
            "Lugar de nacimiento": self.employee.municipality_birth.name,
            "Fecha de nacimiento": self.employee.birthdate.strftime("%d/%m/%Y"),
            "Calle": self.employee.address_street,
            "No": self.employee.address_number,
            "Colonia": self.employee.neighborhood,
            "Municipio": self.employee.municipality.name.split(" / ")[1],
            "Estado": self.employee.municipality.name.split(" / ")[0],
            "No. IMSSS": self.employee.imss,
            "No. INE": self.employee.ine,
            "CURP": self.employee.curp,
            "RFC": self.employee.rfc,
            "Celular personal": self.employee.phone,
            "Telefono de emergencias": self.employee.emergency_phone,
            "Conocimientos": self.employee.knowledge,
            "Habilidades": self.employee.skills,
        }
        
        # Login as admin and get page
        self.client.login(username=self.admin_user, password=self.admin_pass)
        response = self.client.get(self.endpoint)
        
        # Validate employee details
        for report_title, report_value in report_data.items():
            self.assertContains(response, report_title)
            if report_value:
                self.assertContains(response, report_value)
                
        # Validate refs numbers
        for number in refs_numbers:
            ref_index = refs_numbers.index(number)
            ref_title = f"Referencia {ref_index + 1}"
            self.assertContains(response, ref_title)
            self.assertContains(response, number)
            
        # Validate relatives data
        for relative in relatives:
            self.assertContains(response, relative["relationship"])
            self.assertContains(response, relative["last_name_1"])
            self.assertContains(response, relative["last_name_2"])
            self.assertContains(response, relative["name"])
            self.assertContains(response, relative["age"])
            self.assertContains(response, relative["phone"])
            
        # Validate education
        education_name = self.employee.education.name
        self.assertContains(response, f"fill-{education_name}")
        