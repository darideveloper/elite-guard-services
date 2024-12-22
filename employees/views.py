from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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