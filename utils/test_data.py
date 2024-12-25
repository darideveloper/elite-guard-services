import datetime

from django.contrib.auth.models import User

from employees import models as models_employees
from services import models as models_services
from assistance import models as models_assistance


def create_employee() -> models_employees.Employee:
    """ Create a new employee and return it
    
    Returns:
        models_employees.Employee: Employee created
    """
    
    # Get required data
    marital_status = models_employees.MaritalStatus.objects.get(name="Soltero")
    education = models_employees.Education.objects.get(name="Primaria")
    languages_es = models_employees.Language.objects.get(name="Español")
    municipality = models_employees.Municipality.objects.create(
        name="Estado / Municipio"
    )
    neighborhood = models_employees.Neighborhood.objects.create(
        name="Neighborhood"
    )
    
    # Create employee
    employee = models_employees.Employee.objects.create(
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
        tuple:
            str: Username of the user created
            str: Password of the user created
            User: User created
    """
    
    # Create admin user
    password = "admin"
    user = User.objects.create_superuser(
        username="admin",
        email="test@gmail.com",
        password=password,
    )
    
    return user.username, password, user


def create_agreement() -> models_services.Agreement:
    """ Create a new agreement and return it
    
    Returns:
        models_employees.Agreement: Agreement created
    """
    
    # Create agreement
    agreement = models_services.Agreement.objects.create(
        company_name="Company",
        start_date=datetime.date(2021, 1, 1),
        effective_date=datetime.date(2022, 1, 1),
        safety_equipment="Safety equipment",
    )
    
    return agreement


def create_service(
    agreement: models_services.Agreement = None,
    employee: models_employees.Employee = None,
) -> models_services.Service:
    """ Create a new service and return it
    
    Args:
        agreement (models_employees.Agreement): Agreement of the service
        employee (models_employees.Employee): Employee of the service
        
    Returns:
        models_employees.Service: Service created
    """
    
    # Default values
    if agreement is None:
        agreement = create_agreement()
    if employee is None:
        employee = create_employee()
    
    # Get required data
    schedule = models_services.Schedule.objects.create(
        name="Schedule",
        start_time=datetime.time(8, 0),
        end_time=datetime.time(16, 0),
    )
    
    # Create service
    service = models_services.Service.objects.create(
        agreement=agreement,
        schedule=schedule,
        employee=employee,
        location="Location",
        description="Description",
    )
    
    return service


def create_weekly_assistance(
    service: models_services.Service = None
) -> models_assistance.WeeklyAssistance:
    """ Create a new weekly assistance and return it
    
    Args:
        service (models_services.Service): Service of the weekly assistance
        
    Returns:
        models_services.WeeklyAssistance: Weekly assistance created
    """
    
    # Default values
    if service is None:
        service = create_service()
    
    # Create weekly assistance
    weekly_assistance = models_assistance.WeeklyAssistance.objects.create(
        service=service,
    )
    
    return weekly_assistance


def create_assistance(
    service: models_services.Service = None,
    weekly_assistance: models_assistance.WeeklyAssistance = None,
) -> models_assistance.Assistance:
    """ Create a new assistance and return it
    
    Args:
        service (models_services.Service): Service of the assistance
        weekly_assistance (models_services.WeeklyAssistance): Weekly assistance to use
        
    Returns:
        models_services.Assistance: Assistance created
    """
    
    # Default values
    if service is None:
        service = create_service()
    if weekly_assistance is None:
        weekly_assistance = create_weekly_assistance(service)
    
    # Create assistance
    assistance = models_assistance.Assistance.objects.create(
        service=service,
        weekly_assistance=weekly_assistance,
    )
    
    return assistance