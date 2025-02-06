from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings

from utils import test_data
from assistance import models as assistance_models
from employees import models as employees_models


class PayrollTest(TestCase):
    """Test custom properties in model"""

    def setUp(self):

        # Load initial data
        call_command("apps_loaddata")

        self.payroll = test_data.create_payroll()
        today = timezone.now()
        yesterday = today - timezone.timedelta(days=1)
        self.assistance_1 = test_data.create_assistance(
            weekly_assistance=self.payroll.weekly_assistance,
            date=today
        )
        self.assistance_2 = test_data.create_assistance(
            weekly_assistance=self.payroll.weekly_assistance,
            date=yesterday
        )

    def __create_extra__(
        self, category: str, amounts: list[float]
    ) -> assistance_models.ExtraPayment:
        """Create extra payments for the assistance

        Args:
            category (str): category of the extra payment
            amounts (list): amounts of the extra payments
        """
        
        # add two penalties to assistance
        penaly_category = assistance_models.ExtraPaymentCategory.objects.get(
            name=category
        )
        for amount in amounts:
            test_data.create_extra_payment(
                assistance=self.assistance_1, category=penaly_category, amount=amount
            )

    def test_get_day_assistance(self):
        """Valdiate assistance in specific day"""

        # Update monday weekly assistance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.save()

        # Validate monday assistance
        assistance = self.payroll.get_day_assistance("monday")
        self.assertTrue(assistance)

    def test_get_day_assistance_no_assistance(self):
        """Valdiate assistance in specific day without assistance"""

        # Update monday weekly assistance
        self.payroll.weekly_assistance.monday = False
        self.payroll.weekly_assistance.save()

        # Validate monday assistance
        assistance = self.payroll.get_day_assistance("monday")
        self.assertFalse(assistance)

    def test_get_hour_rate(self):
        """Validate hourly rate of the employee"""

        # Update employee and schedule
        employee = self.payroll.weekly_assistance.service.employee
        employee.weekly_rate = 100
        employee.save()
        schedule = self.payroll.weekly_assistance.service.schedule
        schedule.hours = 8
        schedule.weekly_attendances = 5
        schedule.save()

        # Validate hourly rate
        hourly_rate = self.payroll.get_hour_rate()
        self.assertEqual(hourly_rate, 2.5)

    def test_agreement_name(self):
        """Validate agreement name"""

        # Update company name
        company_name = "Company"
        self.payroll.weekly_assistance.service.agreement.company_name = company_name
        self.payroll.weekly_assistance.service.agreement.save()

        # Validate agreement name
        self.assertEqual(self.payroll.agreement_name, company_name)

    def test_employee_name(self):
        """Validate employee name"""

        # Update employee name
        employee_name = ["Name", "Last 1", "Last 2"]
        self.payroll.weekly_assistance.service.employee.name = employee_name[0]
        self.payroll.weekly_assistance.service.employee.last_name_1 = employee_name[1]
        self.payroll.weekly_assistance.service.employee.last_name_2 = employee_name[2]
        self.payroll.weekly_assistance.service.employee.save()

        # Validate employee name
        self.assertEqual(self.payroll.employee_name, " ".join(employee_name))

    def test_weekly_rate(self):
        """Validate weekly rate"""

        # Update weekly rate
        weekly_rate = 100
        self.payroll.weekly_assistance.service.employee.weekly_rate = weekly_rate
        self.payroll.weekly_assistance.service.employee.save()

        # Validate weekly rate
        self.assertEqual(self.payroll.weekly_rate, weekly_rate)

    def test_daily_rate(self):
        """Validate daily rate"""

        # Validate daily rate
        employee = self.payroll.weekly_assistance.service.employee
        employee.weekly_rate = 100
        shcedule = self.payroll.weekly_assistance.service.schedule
        shcedule.weekly_attendances = 5
        employee.save()

        self.assertEqual(self.payroll.daily_rate, 20.0)

    def test_worked_days(self):
        """Validate worked days"""

        # Update assistances in weekly assistance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = False
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Validate worked days
        self.assertEqual(self.payroll.worked_days, 3)

    def test_no_attendance_days(self):
        """Validate no attendance days"""

        # Update assistances in weekly assistance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = False
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5

        # Validate no attendance days
        self.assertEqual(self.payroll.no_attendance_days, 2)

    def test_no_attendance_penalty(self):
        """Validate no attendance penalty"""

        # Update assistances in weekly assistance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = False
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5
        self.payroll.weekly_assistance.service.schedule.save()

        # Validate no attendance penalty
        self.assertEqual(self.payroll.no_attendance_penalty, -2000.0)

    def test_penalties_amount(self):
        """Validate penalties extra amount"""

        self.__create_extra__("Penalización", [10, 20])

        # Validate penalties amount
        self.assertEqual(self.payroll.penalties_amount, -30)
        
    def test_bonuses_amount(self):
        """Validate bonuses extra amount"""

        self.__create_extra__("Bono", [30, 40])

        # Validate penalties amount
        self.assertEqual(self.payroll.bonuses_amount, 70)
        
    def test_other_amount(self):
        """Validate other extra amount"""

        self.__create_extra__("Otro", [50, 60])

        # Validate penalties amount
        self.assertEqual(self.payroll.other_amount, 110)
        
    def test_extra_unpaid_hours_amount(self):
        """ Validate un paid hours amount """
        
        # Update extra unpaid hours
        hour_rate = self.payroll.get_hour_rate()
        self.assistance_1.extra_unpaid_hours = 2
        self.assistance_1.save()
        self.assistance_2.extra_unpaid_hours = 3
        self.assistance_2.save()
        
        # Validate extra unpaid hours amount
        self.assertEqual(
            self.payroll.extra_unpaid_hours_amount,
            int(hour_rate * 5 * 100) / 100 * settings.EXTRA_HOUR_RATE
        )
        
    def test_subtotal(self):
        """Validate payroll subtotal"""
        
        # Update assistances in weekly assistance
        # Only 1 no attendance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = True
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5
        self.payroll.weekly_assistance.service.schedule.save()

        # Update amount required for the subtotal
        self.payroll.weekly_assistance.service.employee.weekly_rate = 2000
        self.__create_extra__("Penalización", [10, 20])
        self.__create_extra__("Bono", [30, 40])
        self.__create_extra__("Otro", [50, 60])
        
        # Update extra unpaid hours
        hour_rate = self.payroll.get_hour_rate()
        self.assistance_1.extra_unpaid_hours = 1
        self.assistance_1.save()
        self.assistance_2.extra_unpaid_hours = 2
        self.assistance_2.save()
        
        # Validate payroll subtotal
        total = 2000 - settings.PENALTY_NO_ATTENDANCE - 30 + 70 + 110 + 3 \
            * hour_rate * settings.EXTRA_HOUR_RATE
        self.assertEqual(self.payroll.subtotal, total)
        
    def test_discount_amount(self):
        """Validate discount amount"""
        
        self.__create_extra__("Descuento por robo o daño", [100, 200])

        # Validate penalties amount
        self.assertEqual(self.payroll.discount_amount, -300)
        
    def test_location(self):
        """Validate location"""
        
        # Update location
        location = "Location"
        self.payroll.weekly_assistance.service.location = location
        self.payroll.weekly_assistance.service.save()
        
        # Validate location
        self.assertEqual(self.payroll.location, location)
        
    def test_bank(self):
        """Validate bank"""
        
        # Update bank
        bank = "Bank"
        bank_obj = employees_models.Bank.objects.create(name=bank)
        self.payroll.weekly_assistance.service.employee.bank = bank_obj
        self.payroll.weekly_assistance.service.employee.save()
        
        # Validate bank
        self.assertEqual(self.payroll.bank, bank)
        
    def test_card_number(self):
        """Validate card number"""
        
        # Update card number
        card_number = "1234567890"
        self.payroll.weekly_assistance.service.employee.card_number = card_number
        self.payroll.weekly_assistance.service.employee.save()
        
        # Validate card number
        self.assertEqual(self.payroll.card_number, card_number)
        
    def test_total(self):
        """Validate total"""
        
        # Update assistances in weekly assistance
        # Only 1 no attendance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = True
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5
        self.payroll.weekly_assistance.service.schedule.save()

        # Update amount required for the subtotal
        self.payroll.weekly_assistance.service.employee.weekly_rate = 2000
        self.__create_extra__("Penalización", [10, 20])
        self.__create_extra__("Bono", [30, 40])
        self.__create_extra__("Otro", [50, 60])
        
        # Update extra unpaid hours
        hour_rate = self.payroll.get_hour_rate()
        self.assistance_1.extra_unpaid_hours = 1
        self.assistance_1.save()
        self.assistance_2.extra_unpaid_hours = 2
        self.assistance_2.save()
        
        subtotal = 2000 - settings.PENALTY_NO_ATTENDANCE - 30 + 70 + 110 + 3 \
            * hour_rate * settings.EXTRA_HOUR_RATE
        
        # Add discounts
        self.__create_extra__("Descuento por robo o daño", [100, 200])
        
        # Update discount loans
        self.payroll.discount_loans = -500
        self.payroll.save()
        
        # Validate total
        self.assertEqual(
            self.payroll.total,
            subtotal - 800
        )
        
    def test_total_0_no_attendance_penalty(self):
        """Validate total when the value is 0
        because of the no attendance penalty"""
        
        # Update assistances in weekly assistance
        # 0 assistances
        self.payroll.weekly_assistance.monday = False
        self.payroll.weekly_assistance.tuesday = False
        self.payroll.weekly_assistance.wednesday = False
        self.payroll.weekly_assistance.thursday = False
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5
        self.payroll.weekly_assistance.service.schedule.save()

        # Update amount required for the subtotal
        self.payroll.weekly_assistance.service.employee.weekly_rate = 2000
        self.__create_extra__("Penalización", [10, 20])
        self.__create_extra__("Bono", [30, 40])
        self.__create_extra__("Otro", [50, 60])
        
        # Update extra unpaid hours
        self.assistance_1.extra_unpaid_hours = 1
        self.assistance_1.save()
        self.assistance_2.extra_unpaid_hours = 2
        self.assistance_2.save()
        
        self.assertEqual(self.payroll.total, 0)
    
    def test_subtotal_0_no_negative(self):
        """ Validate subtotal fixed to 0 if negative """
        
        # Update assistances in weekly assistance
        # 0 assistances
        self.payroll.weekly_assistance.monday = False
        self.payroll.weekly_assistance.tuesday = False
        self.payroll.weekly_assistance.wednesday = False
        self.payroll.weekly_assistance.thursday = False
        self.payroll.weekly_assistance.friday = False
        self.payroll.weekly_assistance.saturday = False
        self.payroll.weekly_assistance.sunday = False
        self.payroll.weekly_assistance.save()

        # Update weekly_attendances
        self.payroll.weekly_assistance.service.schedule.weekly_attendances = 5
        self.payroll.weekly_assistance.service.schedule.save()

        # Validate penalties and subtotal
        self.assertEqual(
            self.payroll.no_attendance_penalty,
            - self.payroll.no_attendance_days * settings.PENALTY_NO_ATTENDANCE
        )
        self.assertEqual(self.payroll.subtotal, 0)
        
    def test_total_0_no_negative(self):
        """ Validate total fixed to 0 if negative """
        
        # Update assistances in weekly assistance
        # full attendance
        self.payroll.weekly_assistance.monday = True
        self.payroll.weekly_assistance.tuesday = True
        self.payroll.weekly_assistance.wednesday = True
        self.payroll.weekly_assistance.thursday = True
        self.payroll.weekly_assistance.friday = True
        self.payroll.weekly_assistance.saturday = True
        self.payroll.weekly_assistance.sunday = True
        self.payroll.weekly_assistance.save()

        # Add discounts
        self.__create_extra__("Descuento por robo o daño", [20000])
        
        # Validate subtotal and total
        self.assertEqual(
            self.payroll.subtotal,
            self.payroll.weekly_rate
        )
        self.assertEqual(self.payroll.total, 0)
        
        