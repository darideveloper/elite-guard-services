from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from utils import test_data
from inventory import models as models_inventory
from employees import models as models_employees


class ItemTransactionModelTestCase(TestCase):
    """ Validate model custom methods """
    
    def setUp(self):
        
        # Create test data
        self.item = test_data.create_item()
        
    def __create_transaction__(self, quantity: int):
        """ Create a new transaction """
        
        return models_inventory.ItemTransaction.objects.create(
            item=self.item,
            quantity=quantity,
            details='This is a test transaction',
        )
        
    def test_no_negative_stock(self):
        """ Test negative stock not allowed """
        
        # Greater than stock
        quantity = -100
        
        # Create transaction
        try:
            self.__create_transaction__(quantity)
        except ValueError as e:
            self.assertEqual(
                str(e),
                'No hay suficiente stock para la transacción. '
                f'Stock actual: {self.item.stock}'
            )
            
    def test_stock_updated(self):
        """ Test item stock updated after transaction """
        
        # Initial stock
        initial_stock = self.item.stock
        
        # Create transaction
        quantity = -2
        self.__create_transaction__(quantity)
        
        # Check stock
        self.assertEqual(
            self.item.stock,
            initial_stock + quantity
        )


class ItemLoanModelTestCase(TestCase):
    """ Validate model custom methods """
    
    def setUp(self):
        
        # Create initial data
        call_command("apps_loaddata")
        
        # Create test data
        self.item = test_data.create_item()
        self.employee = test_data.create_employee()
        self.service = test_data.create_service()
        
    def __create_item_loan__(self, quantity: int = 2):
        """ Create a new loan """
        
        return models_inventory.ItemLoan.objects.create(
            item=self.item,
            quantity=quantity,
            employee=self.employee,
            service=self.service,
            details='This is a test loan',
        )
        
    def test_no_negative_stock(self):
        """ Test negative item stock not allowed """
        
        # Greater than stock
        quantity = 100
        
        # Create loan
        try:
            self.__create_item_loan__(quantity)
        except ValueError as e:
            self.assertEqual(
                str(e),
                'No hay suficiente stock para el préstamo. '
                f'Stock actual: {self.item.stock}'
            )
    
    def test_transaction_created(self):
        """ Test transaction created after loan """
        
        self.__create_item_loan__()
        transaction = models_inventory.ItemTransaction.objects.last()
        self.assertEqual(transaction.item, self.item)
        self.assertEqual(transaction.quantity, -2)
        self.assertEqual(
            transaction.details,
            f'<<Prestamo>>: empleado: {self.employee} - servicio: {self.service} '
            '- detalles: This is a test loan'
        )
        
    def test_stock_updated(self):
        """ Test item stock updated after loan """
        
        # Initial stock
        initial_stock = self.item.stock
        
        # Create loan
        item_loan = self.__create_item_loan__()
        
        # Check stock
        self.assertEqual(
            self.item.stock,
            initial_stock - item_loan.quantity
        )
        
    def test_loan_created(self):
        """ Test employee loan created after item loan """
        
        item_loan = self.__create_item_loan__()
        employee_loan = models_employees.Loan.objects.last()
        time_zone = timezone.get_current_timezone()
        
        self.assertEqual(employee_loan.employee, self.employee)
        self.assertEqual(
            employee_loan.amount,
            item_loan.quantity * self.item.price,
        )
        self.assertEqual(
            employee_loan.date.astimezone(time_zone).date(),
            timezone.now().astimezone(time_zone).date()
        )
        self.assertEqual(
            employee_loan.details,
            f"<<Préstamo>>: item: {self.item} - cantidad: {item_loan.quantity} "
            f"- servicio: {self.service} - detalles: {item_loan.details}",
        )


class ItemAdminTestCase(TestCase):
    """ Validate custom fields and methods in model admin """
    
    def setUp(self):
    
        # Create test data
        self.item = test_data.create_item()
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        self.endpoints = {
            "list": "/admin/inventory/item/",
            "change": f"/admin/inventory/item/{self.item.pk}/change/",
        }
        
    def test_list_total_price(self):
        """ Test custom field total price field in list view """
        
        # Login and get list view response
        self.client.login(
            username=self.admin_user,
            password=self.admin_pass
        )
        response = self.client.get(self.endpoints["list"])
        
        # Check total price field in response
        self.assertContains(response, 'Precio total')
        self.assertContains(response, self.item.price * self.item.stock)
        