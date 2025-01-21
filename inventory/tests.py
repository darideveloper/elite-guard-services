from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone

from utils import test_data
from inventory import models as models_inventory
from employees import models as models_employees


# --------------------
# MODELS TESTS
# --------------------


class ItemTransactionModelTestCase(TestCase):
    """ Validate model custom methods """
    
    def setUp(self):
        
        # Create test data
        self.item = test_data.create_item()
        
    def test_no_negative_stock(self):
        """ Test negative stock not allowed """
        
        # Greater than stock
        quantity = -100
        
        # Create transaction
        try:
            test_data.create_item_transaction(self.item, quantity)
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
        test_data.create_item_transaction(self.item, quantity)
        
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
        
    def test_no_negative_stock(self):
        """ Test negative item stock not allowed """
        
        # Greater than stock
        quantity = 100
        
        # Create loan
        try:
            test_data.create_item_loan(
                self.item,
                self.employee,
                self.service,
                quantity
            )
        except ValueError as e:
            self.assertEqual(
                str(e),
                'No hay suficiente stock para el préstamo. '
                f'Stock actual: {self.item.stock}'
            )
    
    def test_transaction_created(self):
        """ Test transaction created after loan """
        
        test_data.create_item_loan(
            self.item,
            self.employee,
            self.service,
        )
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
        item_loan = test_data.create_item_loan(
            self.item,
            self.employee,
            self.service,
        )
        
        # Check stock
        self.assertEqual(
            self.item.stock,
            initial_stock - item_loan.quantity
        )
        
    def test_loan_created(self):
        """ Test employee loan created after item loan """
        
        item_loan = test_data.create_item_loan(
            self.item,
            self.employee,
            self.service,
        )
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

# --------------------
# ADMIN TESTS
# --------------------


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
        
    def test_change_no_update_stock(self):
        """ Test no update stock directly when save item """
        
        # Login and get change view response
        self.client.login(
            username=self.admin_user,
            password=self.admin_pass
        )
        response = self.client.get(self.endpoints["change"])
        initial_stock = self.item.stock
        
        # Submit form with different stock and follow redirect
        stock = 100
        response = self.client.post(
            self.endpoints["change"],
            {
                "uuid": self.item.uuid,
                "name": self.item.name,
                "details": self.item.details,
                "price": self.item.price,
                "stock": stock,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'No se puede modificar el stock de un artículo directamente'
        )
        self.assertContains(
            response,
            'Por favor, añada una transacción de artículo'
        )
        self.item.refresh_from_db()
        new_stock = self.item.stock
        self.assertEqual(new_stock, initial_stock)
        
        
class ItemTransactionAdminTestCase(TestCase):
    """ Validate custom fields and methods in model admin """
    
    def setUp(self):
    
        # Create test data
        self.item_transaction = test_data.create_item_transaction()
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        self.endpoints = {
            "list": "/admin/inventory/itemtransaction/",
            "change": "/admin/inventory/itemtransaction/"
                      f"{self.item_transaction.id}/change/",
            "add": "/admin/inventory/itemtransaction/add/",
        }
        
    def test_add_no_negative_stock(self):
        """ Test negative stock not allowed when add transaction """
        
        # Login and get change view response
        self.client.login(
            username=self.admin_user,
            password=self.admin_pass
        )
        
        # Submit form with negative quantity and follow redirect
        quantity = -100
        response = self.client.post(
            self.endpoints["add"],
            {
                "item": self.item_transaction.item.pk,
                "quantity": quantity,
                "details": "This is a test transaction",
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'No hay suficiente stock para la transacción.'
        )
        self.assertContains(
            response,
            f'Stock actual: {self.item_transaction.item.stock}'
        )
    
    def test_change_no_update_quantity(self):
        """ Test no update quantity directly when save transaction """
        
        # Login and get change view response
        self.client.login(
            username=self.admin_user,
            password=self.admin_pass
        )
        initial_quantity = self.item_transaction.quantity
        
        # Submit form with different quantity and follow redirect
        quantity = 100
        response = self.client.post(
            self.endpoints["change"],
            {
                "item": self.item_transaction.item.pk,
                "quantity": quantity,
                "details": self.item_transaction.details,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'No se puede modificar la cantidad de una transacción'
        )
        self.assertContains(
            response,
            'Por favor, añada una nueva transacción de artículo'
        )
        self.item_transaction.refresh_from_db()
        new_quantity = self.item_transaction.quantity
        self.assertEqual(new_quantity, initial_quantity)
        
        
class ItemLoanAdminTestCase(TestCase):
    """ Validate custom fields and methods in model admin """
    
    def setUp(self):
        
        # Load initial data
        call_command("apps_loaddata")
    
        # Create test data
        self.item_loan = test_data.create_item_loan()
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        self.endpoints = {
            "list": "/admin/inventory/itemloan/",
            "change": f"/admin/inventory/itemloan/{self.item_loan.id}/change/",
            "add": "/admin/inventory/itemloan/add/",
        }
        
    def test_change_no_update_quantity(self):
        """ Test no update quantity directly when save loan """
        
        # Login and get change view response
        self.client.login(
            username=self.admin_user,
            password=self.admin_pass
        )
        initial_quantity = self.item_loan.quantity
        
        # Submit form with different quantity and follow redirect
        quantity = 100
        response = self.client.post(
            self.endpoints["change"],
            {
                "item": self.item_loan.item.pk,
                "employee": self.item_loan.employee.pk,
                "service": self.item_loan.service.pk,
                "quantity": quantity,
                "details": self.item_loan.details,
            },
            follow=True
        )
        with open("temp.html", "w", encoding="utf-8") as f:
            f.write(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'No se puede modificar la cantidad de un '
            'préstamo de artículo directamente'
        )
        self.assertContains(
            response,
            'Por favor, añada un nuevo préstamo'
        )
        self.item_loan.refresh_from_db()
        new_quantity = self.item_loan.quantity
        self.assertEqual(new_quantity, initial_quantity)
        