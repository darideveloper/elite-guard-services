from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from employees import models

    
class ReportEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "employees/reports/employee.html"
    permission_required = 'auth.is_staff'  # Permission to validate

    def get_context_data(self, **kwargs):
        # Get employee data
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('id')
        employee = models.Employee.objects.get(id=employee_id)
        
        # Add all employee data to the context
        context['employee'] = model_to_dict(employee)
        
        # Caluclated fields
        age = employee.get_age()
        context['employee']["age"] = age
        
        marital_status = employee.marital_status.name
        context['employee']["marital_status"] = marital_status
        
        municipality_birth = employee.municipality_birth.name
        context['employee']["municipality_birth"] = municipality_birth
        
        colony = employee.colony.name
        context['employee']["colony"] = colony
        
        estado, municipio = employee.municipality.name.split(" / ")
        context['employee']["estado"] = estado
        context['employee']["municipio"] = municipio
        
        return context