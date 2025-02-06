from django.core.management.base import BaseCommand
from django.utils import timezone

from assistance import models as assistance_models
from accounting import models as accounting_models
from employees import models as employees_models


class Command(BaseCommand):
    help = "Create a payroll for each wmployee / weekly asistance"

    def handle(self, *args, **options):

        # Get last week of the year
        year = timezone.now().year
        last_weekly_assistance = (
            assistance_models.WeeklyAssistance.objects.filter(start_date__year=year)
            .order_by("week_number")
            .last()
        )

        # End if no weekly assistances
        if last_weekly_assistance is None:
            print("No weekly assistances found")
            return

        last_week_number = last_weekly_assistance.week_number
        print(f"Last week of the year: {last_week_number}")

        # Get weekly assistances of the last week
        weekly_assistances = assistance_models.WeeklyAssistance.objects.filter(
            week_number=last_week_number
        )
        print(f"Found {weekly_assistances.count()} weekly assistances")

        # Create each payroll
        for weekly_assistance in weekly_assistances:

            employee = weekly_assistance.service.employee

            # Skip payroll if already exists
            if accounting_models.Payroll.objects.filter(
                weekly_assistance=weekly_assistance
            ).exists():
                print(f"Payroll for {employee} already exists")
                continue

            # Create new payroll
            payroll = accounting_models.Payroll.objects.create(
                weekly_assistance=weekly_assistance,
            )
            print(f"Created payroll for {employee}")

            # Get current total
            payroll_total = payroll.total
            print(f"\tPayroll total is {payroll_total} for {employee}")

            if payroll_total == 0:
                # Validate pending discounts "Descuento por robo o daño"

                print(f"\tChecking discounts for {employee}")

                # Get discounts total
                assitances = assistance_models.Assistance.objects.filter(
                    weekly_assistance=weekly_assistance
                )
                extra_payment_category = (
                    assistance_models.ExtraPaymentCategory.objects.get(
                        name="Descuento por robo o daño"
                    )
                )
                discounts = assistance_models.ExtraPayment.objects.filter(
                    category=extra_payment_category, assistance__in=assitances
                )

                if not discounts.exists():
                    print(f"\tNo discounts found for {employee}")

                # Get discounts total and notes
                discounts_total = sum([discount.amount for discount in discounts])
                discounts_notes = "".join([
                    f"\n{discount.notes}" for discount in discounts
                ])
                discounts_notes = discounts_notes.strip()

                # Create loan for unpaid discounts
                loan_details = "Descuento por robo o daño."
                if discounts_notes:
                    loan_details += f" Detalles: \n{discounts_notes}"
                    
                employees_models.Loan.objects.create(
                    employee=employee,
                    amount=-discounts_total,
                    details=loan_details,
                )

            else:
                # Discount loans from total

                # Get employee loans
                employee_loans = employees_models.Loan.objects.filter(
                    employee=employee, amount__lt=0
                )
                loans_total = sum([loan.amount for loan in employee_loans])
                print(f"\tTotal employee loans: {loans_total}")

                if abs(loans_total) < payroll_total:
                    # Register a loan total payment
                    employees_models.Loan.objects.create(
                        employee=employee,
                        amount=abs(loans_total),
                        details="Pago de préstamo total por nómina",
                    )
                    discount_loans = loans_total
                else:
                    # Register a loan partial payment
                    employees_models.Loan.objects.create(
                        employee=employee,
                        amount=payroll_total,
                        details="Pago de préstamo parcial por nómina",
                    )
                    discount_loans = -payroll_total

                # Update payroll total
                payroll.discount_loans = discount_loans
                payroll.save()
