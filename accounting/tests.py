from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from bs4 import BeautifulSoup
from utils.dates import get_current_week
from utils import test_data


class PayrollAdminTest(TestCase):
    """Test custom features in admin/payroll """

    def setUp(self):

        # Create initial data
        call_command("apps_loaddata")
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()

        # Create today and last week and last year assistances
        self.weekly_assistances = [
            test_data.create_weekly_assistance(),
            test_data.create_weekly_assistance(),
            test_data.create_weekly_assistance(),
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
        print(">>>>>>>", weeks)

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
