from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from employees import models
from utils.media import get_media_url


class ReportEmployeeDetailsView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView
):
    template_name = "employees/reports/employee-details.html"
    permission_required = 'auth.is_staff'  # Permission to validate

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

        return context


class ReportEmployeePreviewView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView
):
    template_name = "employees/reports/employee-preview.html"
    permission_required = 'auth.is_staff'  # Permission to validate

    def get_context_data(self, **kwargs):
        # Get employee data
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('id')
        employee = models.Employee.objects.get(id=employee_id)

        # Add specific employee data to the context
        last_name = employee.last_name_1
        if employee.last_name_2:
            last_name += " " + employee.last_name_2
        uniform_date = "N/A"
        if employee.uniform_date:
            uniform_date = employee.uniform_date.strftime("%d/%m/%Y")
            
        context['employee_data'] = {
            "Nombre": employee.name.title(),
            "Apellidos": last_name.title(),
            "Servicio": employee.service,
            "Sueldo": f"$ {employee.daily_rate} / dia",
            "Fecha de nacimiento": employee.birthdate.strftime("%d/%m/%Y"),
            "Edad": employee.get_age(),
            "RFC": employee.rfc if employee.rfc else "N/A",
            "CURP": employee.curp if employee.curp else "N/A",
            "IMSS": employee.imss if employee.imss else "N/A",
            "Infonavit": employee.infonavit if employee.infonavit else "N/A",
            "Estado Civil": employee.marital_status.name,
            "Dirección": f"{employee.address_street} {employee.address_number}".title(),
            "Colonia": employee.neighborhood.name,
            "Municipio": employee.municipality.name,
            "C.P.": employee.postal_code,
            "Teléfono": employee.phone,
            "Banco": employee.bank.name if employee.bank else "N/A",
            "Numero de tarjeta": employee.card_number if employee.card_number else "N/A",
            "Fecha de uniforme": uniform_date,
            "Activo": "Si" if employee.status.name == "Activo" else "No",
        }
        
        return context
