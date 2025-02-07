import re
import json

from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.views import View

from employees import models
from services import models as services_models
from utils.media import get_media_url


class ReportEmployeeDetailsView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView
):
    """ Custom view to generate a report with all the details of an employee """

    # Template and permission
    template_name = "employees/reports/employee-details.html"
    permission_required = 'employees.view_employee'

    def get_context_data(self, **kwargs):
        # Get employee data
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('id')
        employee = models.Employee.objects.get(id=employee_id)

        # Add all employee data to the context
        context['employee'] = model_to_dict(employee)

        # Replace none fills with empty strings
        for field_name, value in context['employee'].items():
            if value is None:
                context['employee'][field_name] = ""

        # Caluclated fields
        age = employee.get_age()
        context['employee']["age"] = age

        marital_status = employee.marital_status.name
        context['employee']["marital_status"] = marital_status

        municipality_birth = employee.municipality_birth.name
        context['employee']["municipality_birth"] = municipality_birth

        neighborhood = employee.neighborhood.name
        context['employee']["neighborhood"] = neighborhood

        estado, municipio = employee.municipality.name.split(" / ")
        context['employee']["estado"] = estado
        context['employee']["municipio"] = municipio
        
        context['employee']["status_history"] = employee.status_history

        # add refs contact numbers
        refs = models.Ref.objects.filter(employee=employee)
        refs_numbers = []
        for ref in refs:
            if ref.phone:
                refs_numbers.append(ref.phone)
        context["refs_numbers"] = refs_numbers

        # Get family data
        relatives = models.Relative.objects.filter(employee=employee)
        relatives_data = []
        for relative in relatives:
            relative_data = model_to_dict(relative)
            relative_data["relationship"] = relative.relationship.name
            relatives_data.append(relative_data)
        context['relatives'] = relatives_data

        # add education options and selected
        education_options = models.Education.objects.all()
        education_options_names = []
        for option in education_options:
            education_options_names.append(option.name)
        context["education_options"] = education_options_names
        education = employee.education.name
        context["education"] = education

        # Add created at date
        context['employee']["created_at"] = employee.created_at

        # add photo
        if employee.photo:
            context["photo"] = get_media_url(employee.photo)

        # Auto print
        context["auto_print"] = True

        # Service data
        service = services_models.Service.objects.filter(employee=employee)
        if service:
            service = service[0]
            description = service.description
            location = service.location
            company = service.agreement.company_name
            schedule = service.schedule.name
            context["service"] = {
                "description": description,
                "location": location,
                "company": company,
                "schedule": schedule
            }
        else:
            context["service"] = {
                "description": "N/A",
                "location": "N/A",
                "company": "N/A",
                "schedule": "N/A"
            }

        return context


class ApiValidateCurpView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    """ Endpoint to validate CURP from an employee """

    permission_required = 'employees.view_employee'

    def valid_curp(self, curp):
        # Regular expression to validate the general CURP format
        curp_regex = r"^([A-Z]{4}\d{6}[HM]" \
                     r"(?:AS|BC|BS|CC|CL|CM|CS|CH|DF|GR|GT|HG|JC|MC|MS|MN|" \
                     r"NT|OC|PL|QR|SL|SP|TC|TL|VZ|YN|ZS)" \
                     r"[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$"
        matched = re.match(curp_regex, curp)

        # Check if it matches the general format
        if not matched:
            return False

        # Function to calculate the verification digit
        def verification_digit(curp17):
            dictionary = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            total_sum = 0
            for i, char in enumerate(curp17):
                total_sum += dictionary.index(char) * (18 - i)
            digit = 10 - total_sum % 10
            return 0 if digit == 10 else digit

        # Check if the verification digit matches
        curp17 = matched.group(1)
        calculated_digit = verification_digit(curp17)
        provided_digit = int(matched.group(2))

        return calculated_digit == provided_digit

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        curp = json_data.get("curp")

        # Validate curp length
        if len(curp) != 18:
            return JsonResponse({
                "status": "error",
                "message": "El CURP debe tener 18 caracteres",
                "data": {}
            }, status=400)

        # Validate curp format
        is_valid = self.valid_curp(curp)
        if not is_valid:
            return JsonResponse({
                "status": "error",
                "message": "El CURP proporcionado no es válido",
                "data": {}
            }, status=400)

        # Validate if the curp already exists
        employee = models.Employee.objects.filter(curp=curp)
        if employee:
            return JsonResponse({
                "status": "error",
                "message": "Ya existe un empleado con el CURP proporcionado",
                "data": {
                    "employee_id": employee[0].id
                }
            }, status=400)

        return JsonResponse({
            "status": "success",
            "message": "CURP válido",
            "data": {}
        })
