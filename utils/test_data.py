import datetime

from django.contrib.auth.models import User

from employees import models


def create_employee() -> models.Employee:
    """ Create a new employee and return it
    
    Returns:
        models.Employee: Employee created
    """
    
    # Get required data
    marital_status = models.MaritalStatus.objects.get(name="Soltero")
    education = models.Education.objects.get(name="Primaria")
    languages_es = models.Language.objects.get(name="Español")
    municipality = models.Municipality.objects.create(
        name="Estado / Municipio"
    )
    neighborhood = models.Neighborhood.objects.create(
        name="Neighborhood"
    )
    
    # Create employee
    employee = models.Employee.objects.create(
        name="John",
        last_name_1="Doe",
        height=1.70,
        weight=70,
        marital_status=marital_status,
        education=education,
        birthdate=datetime.date(1990, 1, 1),
        municipality_birth=municipality,
        daily_rate=100,
        curp="test CURP",
        ine="test INE",
        knowledge="Knowledge",
        skills="Skills",
        municipality=municipality,
        neighborhood=neighborhood,
        postal_code="12345",
        address_street="Street",
        address_number="1987",
        phone="0000000000",
        emergency_phone="0000000001",
    )
    employee.languages.add(languages_es)
    employee.save()
    
    return employee


def create_admin_user() -> tuple[str, str]:
    """ Create a new admin user and return it
    
    Returns:
        tuple[str, str]: Username and password of the user created
    """
    
    # Create admin user
    password = "admin"
    user = User.objects.create_superuser(
        username="admin",
        email="test@gmail.com",
        password=password,
    )
    
    return user.username, password