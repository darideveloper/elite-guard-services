from time import sleep
from io import BytesIO

import openpyxl
from django.test import TestCase, LiveServerTestCase
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

from assistance import models
from utils import test_data
from utils.dates import get_week_day, get_current_week
from utils.automation import get_selenium_elems
from core.test_base.test_admin import TestAdminBase


class AssistanceModelTest(TestCase):
    """Test custom methods in assistance model"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")

        # Create initial data
        self.weekly_assistance = test_data.create_weekly_assistance()
        assistance_1 = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )
        yesterday = assistance_1.date - timezone.timedelta(days=1)
        assistance_2 = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance, date=yesterday
        )
        self.assistances = [assistance_1, assistance_2]

    def test_save_update_weekly_date_status(self):
        """Validate day status updated in weekly assistance
        when change assistance status"""

        # Update assistance status
        self.assistances[0].attendance = True
        self.assistances[0].save()
        week_day = get_week_day(self.assistances[0].date, "en")

        # Valdiate weekly assistance status
        self.weekly_assistance.refresh_from_db()
        self.assertTrue(getattr(self.weekly_assistance, week_day))

    def test_save_update_weekly_paid_hours(self):
        """Validate weekly paid hours updated in weekly assistance
        when update assistance"""

        # Update assistance
        self.assistances[0].extra_paid_hours = 2
        self.assistances[0].save()
        self.assistances[1].extra_paid_hours = 3
        self.assistances[1].save()

        # Valdiate weekly assistance status
        self.weekly_assistance.refresh_from_db()
        self.assertEqual(self.weekly_assistance.total_extra_paid_hours, 5)

    def test_save_update_weekly_unpaid_hours(self):
        """Validate weekly unpaid hours updated in weekly assistance
        when update assistance"""

        # Update assistance
        self.assistances[0].extra_unpaid_hours = 2
        self.assistances[0].save()
        self.assistances[1].extra_unpaid_hours = 3
        self.assistances[1].save()

        # Valdiate weekly assistance status
        self.weekly_assistance.refresh_from_db()
        self.assertEqual(self.weekly_assistance.total_extra_unpaid_hours, 5)

    def test_save_update_weekly_notes(self):
        """valdiate weekly notes updated in weekly assistance
        when update assistance"""

        # Update assistance
        self.assistances[0].notes = "note 1"
        self.assistances[0].save()
        self.assistances[1].notes = "note 2"
        self.assistances[1].save()

        # Valdiate weekly assistance status
        self.weekly_assistance.refresh_from_db()
        self.assertEqual(self.weekly_assistance.notes, "note 1\nnote 2")


class AssistanceAdminTest(TestCase):
    """Test custom features in admin/assistance"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()

        # Create today assistance
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistances = []
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )
        self.assistances.append(assistance)

        # Create yesterday assistance
        yesterday = assistance.date - timezone.timedelta(days=1)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=yesterday,
        )
        self.assistances.append(assistance)

        # Create last year assistance
        last_year = assistance.date - timezone.timedelta(days=365)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=last_year,
        )
        self.assistances.append(assistance)

        self.endpoint = "/admin/assistance/assistance/"

    def test_custom_field_company(self):
        """Validate "company name" custom field in list view"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)

        # Validate company name
        self.assertContains(
            response,
            self.weekly_assistance.service.agreement.company_name,
        )

    def test_custom_field_employee(self):
        """Validate "employee name" custom field in list view"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)

        # Validate company name
        self.assertContains(
            response,
            str(self.weekly_assistance.service.employee),
        )

    def test_custom_actions(self):
        """Validate custom actions in list view"""

        links = {
            "Ver extras": "/admin/assistance/extrapayment/?assistance__id__exact=1",
            "Añadir extra": "/admin/assistance/extrapayment/add/?assistance=1",
        }

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)

        # Validate links
        for link_text, link in links.items():
            self.assertContains(response, link_text)
            self.assertContains(response, link)

    def test_custom_filters_options(self):
        """Validate custom filters options in admin"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")

        # Validate years
        years = list(set([assistance.date.year for assistance in self.assistances]))

        year_options = soup.select('option[data-name="year"]')
        for option in year_options:
            self.assertIn(int(option.text), years)

        # Validate dates options
        options = [
            "hoy",
            "todas las fechas (filtrar por año y semana)",
        ]
        date_options = soup.select('option[data-name="date"]')
        for option in date_options:
            self.assertIn(option.text.lower().strip(), options)

    def test_custom_filters_default(self):
        """Validate custom filters default option in admin"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")

        # Validate years filter
        current_year = timezone.now().year
        year_selected = soup.select_one('option[data-name="year"][selected]')
        self.assertEqual(int(year_selected.text), current_year)

        # Validate today filter
        today_option = soup.select_one('option[data-name="date"][selected]')
        self.assertIn("hoy", today_option.text.lower())

        # Validate only today registers
        rows = soup.select('tr[role="row"]')
        self.assertEqual(len(rows), 1)


class WeeklyAssistanceTest(TestCase):
    """ validate custom methods in WeeklyAssistance model """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        
        # Create 2 assistances
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistance_1 = test_data.create_assistance(
            date=today,
            weekly_assistance=self.weekly_assistance,
            attendance=True,
        )
        self.assistance_2 = test_data.create_assistance(
            date=yesterday,
            weekly_assistance=self.weekly_assistance,
            attendance=True,
        )
        self.assistance_1.save()
        self.assistance_2.save()
        
    def test_get_worked_days(self):
        """ Validate 2 worked days in weekly assistance """
        
        worked_days = self.weekly_assistance.get_worked_days()
        self.assertEqual(worked_days, 2)
        
    def test_no_attendance_days(self):
        """ Validate no attendance days based in shcedule weekly_attendances """
        
        weekly_attendances = self.weekly_assistance.service.schedule.weekly_attendances
        worked_days = self.weekly_assistance.get_worked_days()
        no_attendance_days = weekly_attendances - worked_days
        self.assertEqual(
            self.weekly_assistance.get_no_attendance_days(),
            no_attendance_days
        )
        
    def test_no_attendance_days_no_negative(self):
        """ Validate no attendance days based in shcedule weekly_attendances
        with no negative value (employee worked more than weekly attendances)
        """
        
        weekly_attendances = 0
        self.weekly_assistance.service.schedule.weekly_attendances = weekly_attendances
        self.weekly_assistance.service.schedule.save()
        self.assertEqual(
            self.weekly_assistance.get_no_attendance_days(),
            0
        )
        

class WeeklyAssistanceAdminTest(TestCase):
    """Test custom features in admin/weekly-assistance"""

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

        # Create today assistance
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistances = []
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )
        self.assistances.append(assistance)

        # Create yesterday assistance
        yesterday = assistance.date - timezone.timedelta(days=1)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=yesterday,
        )
        self.assistances.append(assistance)

        # Create last year assistance
        last_year = assistance.date - timezone.timedelta(days=365)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=last_year,
        )
        self.assistances.append(assistance)

        self.endpoint = "/admin/assistance/weeklyassistance/"

    def test_custom_filters_options(self):
        """Validate custom filters options in admin"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")

        # Validate years
        years = list(set([assistance.date.year for assistance in self.assistances]))

        year_options = soup.select('option[data-name="year"]')
        for option in year_options:
            self.assertIn(int(option.text), years)

        # Validate week number
        weeks = list(
            set(
                [
                    assistance.weekly_assistance.week_number
                    for assistance in self.assistances
                ]
            )
        )

        weeks_options = soup.select(
            'option[data-name="weekly_assistance__week_number"]'
        )
        for option in weeks_options:
            self.assertIn(int(option.value), weeks)

    def test_custom_filters_default(self):
        """Validate custom filters default option in admin"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")

        # Validate years filter
        current_year = timezone.now().year
        year_selected = soup.select_one('option[data-name="year"][selected]')
        self.assertEqual(int(year_selected.text), current_year)

        # Validate week number filter
        current_week = get_current_week()
        week_selected = soup.select_one('option[data-name="week_number"]' "[selected]")
        self.assertEqual(int(week_selected["value"]), current_week)
        self.assertEqual(week_selected.text.strip(), f"Semana actual ({current_week})")

    def test_custom_field_company_name(self):
        """Validate "company name" custom field in list view"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)

        # Validate company name
        self.assertContains(
            response,
            self.agreement.company_name,
        )

    def test_custom_field_employee(self):
        """Validate "employee name" custom field in list view"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        response = self.client.get(self.endpoint)

        # Validate company name
        self.assertContains(
            response,
            str(self.employee),
        )

    def test_custom_field_custom_links(self):
        """Validate custom links in list view"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open employee list page
        sleep(2)
        response = self.client.get(self.endpoint)

        # Validate custom links
        link_data = {
            "Editar Dias": [
                self.employee.id,
                self.weekly_assistance.week_number,
                self.weekly_assistance.start_date.year,
                "all",
            ]
        }

        # Validate button texts and links content
        for link_text, link_values in link_data.items():
            self.assertContains(response, link_text)
            for value in link_values:
                self.assertContains(response, f"={value}")

    def test_action_export_excel(self):
        """Validate excel generated in export action"""

        # Generate excel
        self.client.login(username=self.admin_user, password=self.admin_pass)
        response = self.client.post(
            self.endpoint,
            {"action": "export_excel", "_selected_action": [self.weekly_assistance.id]},
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("Content-Disposition", response)
        self.assertIn(
            "attachment; filename=export.xlsx", response["Content-Disposition"]
        )

        workbook = openpyxl.load_workbook(BytesIO(response.content))
        worksheet = workbook.active

        # Check the sheet title
        self.assertEqual(
            worksheet.title, f"Asistencias Semana {self.weekly_assistance.week_number}"
        )

        # Check header and data row
        header = self.weekly_assistance.get_data_header()
        data_row = self.weekly_assistance.get_data_list()
        self.assertEqual([cell.value for cell in worksheet[1]], header)
        self.assertEqual([cell.value for cell in worksheet[2]], data_row)


class WeeklyAssistanceAdminSeleniumTest(LiveServerTestCase):

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

        # Create today assistance
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistances = []
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )
        self.assistances.append(assistance)

        # Create yesterday assistance
        yesterday = assistance.date - timezone.timedelta(days=1)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=yesterday,
        )
        self.assistances.append(assistance)

        # Create last year assistance
        last_year = assistance.date - timezone.timedelta(days=365)
        assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance,
            date=last_year,
        )
        self.assistances.append(assistance)

        self.endpoint = "/admin/assistance/weeklyassistance/"

        self.__setup_selenium__()
        self.__login__()

    def tearDown(self):
        """Close selenium"""
        try:
            self.driver.quit()
        except Exception:
            pass

    def __setup_selenium__(self):
        """Setup and open selenium browser"""

        chrome_options = Options()
        if settings.TEST_HEADLESS:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def __login__(self):
        """Login and load main page"""

        # Load login page and get fields
        self.driver.get(f"{self.live_server_url}/admin/")
        sleep(2)
        selectors_login = {
            "username": "input[name='username']",
            "password": "input[name='password']",
            "submit": "button[type='submit']",
        }
        fields_login = get_selenium_elems(self.driver, selectors_login)

        fields_login["username"].send_keys(self.admin_user)
        fields_login["password"].send_keys(self.admin_pass)
        fields_login["submit"].click()

        # Wait after login
        sleep(3)

        # Open page
        self.driver.get(f"{self.live_server_url}{self.endpoint}")

    def test_default_action(self):
        """Validate to have the export_excel action as default with js"""

        # Get data
        selectors = {"select_action_value": 'select[name="action"] + span'}
        values = get_selenium_elems(self.driver, selectors)
        self.assertEqual(values["select_action_value"].text, "Exportar a Excel")

    def test_all_rows_selected(self):
        """Validate all rows selected by default"""

        sleep(2)
        selector_checkboxes = "input.action-select"
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, selector_checkboxes)
        for checkbox in checkboxes:
            self.assertTrue(checkbox.is_selected())


class CommandCreateWeeklyAssistanceTest(TestCase):
    """Test running the command create_weekly_assistance"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")

        # Create service
        self.service = test_data.create_service()

    def test_run_with_service(self):
        """Validate the command create_weekly_assistance regular runnign"""

        # Run command
        call_command("create_weekly_assistance")

        # Validate weekly assistance created and content
        weekly_assistance = models.WeeklyAssistance.objects.first()
        self.assertIsNotNone(weekly_assistance)
        self.assertEqual(weekly_assistance.week_number, get_current_week())
        self.assertEqual(weekly_assistance.service, self.service)

    def test_run_no_service(self):
        """Validate command create_weekly_assistance without services
        (no weekly assistance created)"""

        # Delete all services
        self.service.delete()

        # Run command
        call_command("create_weekly_assistance")

        # Validate no weekly assistance created
        weekly_assistance = models.WeeklyAssistance.objects.all()
        self.assertEqual(len(weekly_assistance), 0)


class CommandCreateAssistanceTest(TestCase):
    """Test running the command create_assistance"""

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")

        # Create service
        self.service = test_data.create_service()
        self.weekly_assistance = test_data.create_weekly_assistance(
            service=self.service
        )

    def test_run_with_service(self):
        """Validate the command create_assistance regular runnign"""

        # Run command
        call_command("create_assistance")

        # Validate weekly assistance created and content
        time_zone = timezone.get_current_timezone()
        assistance = models.Assistance.objects.first()
        self.assertIsNotNone(assistance)
        self.assertEqual(assistance.date, timezone.now().astimezone(time_zone).date())
        self.assertEqual(
            assistance.weekly_assistance.service, self.weekly_assistance.service
        )
        self.assertEqual(assistance.weekly_assistance.week_number, get_current_week())
        self.assertEqual(assistance.weekly_assistance.start_date.weekday(), 3)

    def test_run_no_service(self):
        """Validate command create_assistance without services
        (no assistance created)"""

        # Delete all services
        self.service.delete()

        # Run command
        call_command("create_assistance")

        # Validate no weekly assistance created
        assistance = models.Assistance.objects.all()
        self.assertEqual(len(assistance), 0)

    def test_run_no_weekly_assistance(self):
        """Validate command create_assistance without weekly assistance
        (assistance and weekly asistance created)"""

        # Delete all services
        models.WeeklyAssistance.objects.all().delete()

        # Run command
        call_command("create_assistance")

        # Validate weekly assistances created
        weekly_assistance = models.WeeklyAssistance.objects.all()
        self.assertEqual(len(weekly_assistance), 1)

        # Validate week number in weekly assistance
        weekly_assistance = weekly_assistance[0]
        current_week = get_current_week()
        self.assertEqual(weekly_assistance.week_number, current_week)

        # Validate start date in weekly assistance
        week_start_date = weekly_assistance.start_date
        week_start_date_num = week_start_date.weekday()
        self.assertEqual(week_start_date_num, 3)

        # Validate no weekly assistance created
        assistance = models.Assistance.objects.all()
        self.assertEqual(len(assistance), 1)
        assistance = assistance[0]
        self.assertEqual(assistance.weekly_assistance, weekly_assistance)


class ExtraPaymentAdminSeleniumTest(TestAdminBase):
    """ Test custom features in admin/extra-payment """

    def setUp(self):
        """Load data, setup and login in each test"""

        super().setUp("/admin/assistance/extrapayment/")

        # Create initial data
        self.weekly_assistance = test_data.create_weekly_assistance()
        self.assistance = test_data.create_assistance(
            weekly_assistance=self.weekly_assistance
        )

    def test_go_back_extra(self):
        """ Validate 'Guardar y regresar' button when adding extra payment
        with custom admin action
        """
        
        # Load assistance page
        self.driver.get(f"{self.live_server_url}/admin/assistance/assistance/")
        
        # Click in "Añadir extra" link
        selectors = {
            "add_extra_btn": ".field-custom_links a:nth-child(2)",
        }
        elems = self.get_selenium_elems(selectors)
        elems["add_extra_btn"].click()
        
        # Validate redirect to new page
        sleep(2)
        self.assertIn(
            f"/admin/assistance/extrapayment/add/?assistance={self.assistance.id}",
            self.driver.current_url
        )
        
        # Fill form
        selectors = {
            "category": '.field-category select',
            "amount": '.field-amount input',
            "notes": '.field-notes textarea',
            "save_and_go_back": '[value="Guardar y regresar"]',
        }
        elems = self.get_selenium_elems(selectors)
        self.select_set_value(selectors["category"], "1")
        elems["amount"].send_keys("100")
        elems["notes"].send_keys("Test notes")
        
        # Save and go back
        elems["save_and_go_back"].click()
        sleep(3)
        
        # Validate redirect to assistance page
        self.assertEqual(
            f"{self.live_server_url}/admin/assistance/assistance/",
            self.driver.current_url
        )