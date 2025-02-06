from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from bs4 import BeautifulSoup
from utils.dates import get_current_week
from utils import test_data
from core.test_base.test_admin import TestAdminBase


class PayrollAdminTest(TestCase):
    """Test custom features in admin/payroll """

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()

        # Create today and last week and last year assistances
        self.weekly_assistances = [
            test_data.create_weekly_assistance() for _ in range(4)
        ]
        current_week = get_current_week()
        last_year = timezone.now() - timezone.timedelta(days=365)
        self.weekly_assistances[0].week_number = current_week - 1
        self.weekly_assistances[0].save()
        self.weekly_assistances[1].start_date = last_year
        self.weekly_assistances[1].end_date = last_year
        self.weekly_assistances[1].save()

        # Create Parolls
        self.payrolls = []
        for weekly_assistance in self.weekly_assistances:
            self.payrolls.append(
                test_data.create_payroll(weekly_assistance=weekly_assistance)
            )

        self.endpoint = "/admin/accounting/payroll/"

    def test_custom_filters_options(self):
        """Validate custom filters options in admin"""

        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")

        # Validate years
        years = list(set([
            assistance.start_date.year for assistance in self.weekly_assistances
        ]))

        year_options = soup.select('option[data-name="year"]')
        for option in year_options:
            self.assertIn(int(option.text), years)

        # Validate week number
        weeks = list(
            set(
                [
                    assistance.week_number
                    for assistance in self.weekly_assistances
                ]
            )
        )

        weeks_options = soup.select(
            'option[data-name="week_number"]'
        )
        weeks_options_values = [int(option["value"]) for option in weeks_options]
        for option in weeks_options_values:
            self.assertIn(option, weeks)

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

    def test_custom_filters_no_duplicated_week_number(self):
        """ Validate no duplicated week number in admin filter """
        
        # Login as admin
        self.client.login(username=self.admin_user, password=self.admin_pass)

        # Open list page
        response = self.client.get(self.endpoint)
        soup = BeautifulSoup(response.content, "html.parser")
         
        # Validate week numbers
        weeks_options = soup.select(
            'option[data-name="week_number"]'
        )
        weeks_options_values = [int(option["value"]) for option in weeks_options]
        
        self.assertEqual(
            len(weeks_options_values),
            len(set(weeks_options_values))
        )
        

class PayrollAdminSeleniumTest(TestAdminBase):
    """ Test Payroll admin customization and mtehods """
    
    def setUp(self):
        
        # Set enpoint
        super().setUp("/admin/accounting/payroll/")
   
        # Create payrolls
        test_data.create_payroll()
        test_data.create_payroll(skip_payment=True)
        
    def test_highlight_skip_payment(self):
        """ Test highlight skip payment """
        
        # Check highlight class
        selectors = {
            "hightlight_row": 'tr.highlight-row',
        }
        elems = self.get_selenium_elems(selectors)
        self.assertEqual(len(elems), 1)