from django.test import TestCase
from django.core.management import call_command

from accounting import models as accounting_models
from employees import models as employees_models
from assistance import models as assistance_models
from utils import test_data


class CommandCreatePayrolls(TestCase):
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        employees_num = 2
        self.weekly_assistances = []
        for employee_num in range(employees_num):
            
            employee = test_data.create_employee(
                curp=f"CURP{employee_num}",
                ine=f"INE{employee_num}",
                phone=f"PHONE{employee_num}",
            )
            
            service = test_data.create_service(
                employee=employee,
            )
            
            weekly_assistance = test_data.create_weekly_assistance(
                service=service,
            )
            self.weekly_assistances.append(weekly_assistance)
           
            # Create assistances
            test_data.create_assistance(
                service=service,
                weekly_assistance=weekly_assistance,
            )
            
    def test_run_with_weekly_assistance(self):
        """ Validate two create 2 payrolls """
        
        call_command("create_payrolls")
        
        # Validate payrolls created
        payrolls = accounting_models.Payroll.objects.all()
        self.assertEqual(payrolls.count(), 2)
        
        # Valdiate payroll data
        for weekly_assistance in self.weekly_assistances:
            payroll = accounting_models.Payroll.objects.filter(
                weekly_assistance=weekly_assistance
            )
            self.assertEqual(payroll.count(), 1)
            
    def test_run_without_weekly_assistance(self):
        """ Validate no payrolls created """
        
        # Delete weekly assistances
        for weekly_assistance in self.weekly_assistances:
            weekly_assistance.delete()
        
        call_command("create_payrolls")
        
        # Validate no payrolls created
        payrolls = accounting_models.Payroll.objects.all()
        self.assertEqual(payrolls.count(), 0)
    
    def test_run_create_discount_loan_amount(self):
        """ Create an employee loan if the payroll total is 0
        and the employee has a "Descuento por robo o daño" extra payment.
        validate only amount
        """
        
        # Note: by default the total is 0 because no attendance
    
        # Get main data
        discount_amount = 500
        weekly_assistance = self.weekly_assistances[0]
        assistance = assistance_models.Assistance.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
        employee = weekly_assistance.service.employee
        
        # Create extra payment
        extra_payment_category = assistance_models.ExtraPaymentCategory.objects.get(
            name="Descuento por robo o daño"
        )
        test_data.create_extra_payment(
            category=extra_payment_category,
            assistance=assistance,
            amount=discount_amount,
        )
        
        # Run command
        call_command("create_payrolls")
        
        # Get payroll and employee
        payroll = accounting_models.Payroll.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
                
        # Validate payroll total
        self.assertEqual(payroll.total, 0)
        
        # Validate loan created
        loans = employees_models.Loan.objects.filter(
            employee=employee,
        )
        self.assertEqual(loans.count(), 1)
        loan = loans.first()
        self.assertEqual(float(loan.amount), -discount_amount)
        self.assertEqual(loan.details, "Descuento por robo o daño.")

    def test_run_create_discount_loan_details(self):
        """ Create an employee loan if the payroll total is 0
        and the employee has a "Descuento por robo o daño" extra payment.
        validate only details
        """
        
        # Note: by default the total is 0 because no attendance
    
        # Get main data
        weekly_assistance = self.weekly_assistances[0]
        assistance = assistance_models.Assistance.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
        employee = weekly_assistance.service.employee
        details = [
            "Robo de herramientas.",
            "Daño de herramientas.",
        ]
        
        # Create extra payment
        extra_payment_category = assistance_models.ExtraPaymentCategory.objects.get(
            name="Descuento por robo o daño"
        )
        for detail in details:
            test_data.create_extra_payment(
                category=extra_payment_category,
                assistance=assistance,
                amount=100,
                notes=detail,
            )
        
        # Run command
        call_command("create_payrolls")
        
        # Get payroll and employee
        payroll = accounting_models.Payroll.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
                
        # Validate payroll total
        self.assertEqual(payroll.total, 0)
        
        # Validate loan created
        loans = employees_models.Loan.objects.filter(
            employee=employee,
        )
        self.assertEqual(loans.count(), 1)
        loan = loans.first()
        details_text = "Descuento por robo o daño. Detalles: "
        details_text += "".join([f"\n{detail}" for detail in details])
        self.assertEqual(loan.details, details_text)

    def test_run_create_pay_loan_total_greater(self):
        """ Create a pay register in loans if the payroll total
        if greater than the loans amount.
        """
            
        # Get main data
        weekly_assistance = self.weekly_assistances[0]
        employee = weekly_assistance.service.employee
        
        # Update assistance to have a total of payroll
        weekly_assistance.monday = True
        weekly_assistance.tuesday = True
        weekly_assistance.wednesday = True
        weekly_assistance.thursday = True
        weekly_assistance.friday = True
        weekly_assistance.saturday = True
        weekly_assistance.sunday = True
        weekly_assistance.save()
        
        # Create loan to employee
        loan_amount = 50
        employees_models.Loan.objects.create(
            employee=employee,
            amount=-loan_amount,
            details="Descuento de prueba",
        )
        
        # Create payrolls and get current
        call_command("create_payrolls")
        payroll = accounting_models.Payroll.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
        
        # Validate total
        self.assertEqual(payroll.total, 100.0 - loan_amount)
        
        # Validate loan paid
        loans = employees_models.Loan.objects.filter(
            employee=employee,
        )
        self.assertEqual(loans.count(), 2)
        loans_total = sum([loan.amount for loan in loans])
        self.assertEqual(loans_total, 0)
        loan_paid = employees_models.Loan.objects.get(
            employee=employee,
            amount=loan_amount,
        )
        self.assertEqual(loan_paid.details, "Pago de préstamo total por nómina")
    
    def test_run_create_pay_loan_total_equal(self):
        """ Create a pay register in loans if the payroll total
        if greater than the loans amount.
        """
            
        # Get main data
        weekly_assistance = self.weekly_assistances[0]
        employee = weekly_assistance.service.employee
        
        # Update assistance to have a total of payroll
        weekly_assistance.monday = True
        weekly_assistance.tuesday = True
        weekly_assistance.wednesday = True
        weekly_assistance.thursday = True
        weekly_assistance.friday = True
        weekly_assistance.saturday = True
        weekly_assistance.sunday = True
        weekly_assistance.save()
        
        # Create loan to employee
        loan_amount = 100
        employees_models.Loan.objects.create(
            employee=employee,
            amount=-loan_amount,
            details="Descuento de prueba",
        )
        
        # Create payrolls and get current
        call_command("create_payrolls")
        payroll = accounting_models.Payroll.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
        
        # Validate total
        self.assertEqual(payroll.total, 0)
        
        # Validate loan paid
        loans = employees_models.Loan.objects.filter(
            employee=employee,
        )
        self.assertEqual(loans.count(), 2)
        loans_total = sum([loan.amount for loan in loans])
        self.assertEqual(loans_total, 0)
        loan_paid = employees_models.Loan.objects.get(
            employee=employee,
            amount=loan_amount,
        )
        self.assertEqual(loan_paid.details, "Pago de préstamo parcial por nómina")
        
    def test_run_create_pay_loan_partial(self):
        """ Create a pay register in loans if the payroll total
        if lower than the loans amount.
        """
            
        # Get main data
        weekly_assistance = self.weekly_assistances[0]
        employee = weekly_assistance.service.employee
        
        # Update assistance to have a total of payroll
        weekly_assistance.monday = True
        weekly_assistance.tuesday = True
        weekly_assistance.wednesday = True
        weekly_assistance.thursday = True
        weekly_assistance.friday = True
        weekly_assistance.saturday = True
        weekly_assistance.sunday = True
        weekly_assistance.save()
        
        # Create loan to employee
        loan_amount = 150
        employees_models.Loan.objects.create(
            employee=employee,
            amount=-loan_amount,
            details="Descuento de prueba",
        )
        
        # Create payrolls and get current
        call_command("create_payrolls")
        payroll = accounting_models.Payroll.objects.filter(
            weekly_assistance=weekly_assistance
        ).first()
        
        # Validate total
        self.assertEqual(payroll.total, 0)
        
        # Validate loan paid
        loans = employees_models.Loan.objects.filter(
            employee=employee,
        )
        self.assertEqual(loans.count(), 2)
        loans_total = sum([loan.amount for loan in loans])
        self.assertEqual(float(loans_total), -50)
        loan_paid = employees_models.Loan.objects.get(
            employee=employee,
            amount=100,
        )
        self.assertEqual(loan_paid.details, "Pago de préstamo parcial por nómina")
        
        