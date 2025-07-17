from django.urls import path
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from employees import models
from services import models as services_models


@admin.register(models.Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    """Neighborhood model admin"""

    list_display = ("name",)


@admin.register(models.Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    """Municipality model admin"""

    list_display = ("name",)


@admin.register(models.MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    """MaritalStatus model admin"""

    list_display = ("name",)


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """Status model admin"""

    list_display = ("name",)


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    """Bank model admin"""

    list_display = ("name",)


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Employee model admin"""

    list_display = (
        "created_at",
        "name",
        "last_name_1",
        "last_name_2",
        "weekly_rate",
        "birthdate",
        "status",
        "code",
        "is_eventual",
        "custom_links",
    )
    search_fields = (
        "name",
        "last_name_1",
        "curp",
        "rfc",
        "imss",
        "infonavit",
        "ine",
        "phone",
        "anti_doping_results",
        "administrative_comments",
    )
    list_filter = (
        "marital_status",
        "education",
        "municipality_birth",
        "status",
        "municipality",
        "neighborhood",
        "bank",
        "created_at",
        "updated_at",
    )
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at", "status_history", "balance")
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                    "last_name_1",
                    "last_name_2",
                    "curp",
                    "ine",
                    "height",
                    "weight",
                    "marital_status",
                    "education",
                    "languages",
                    "photo",
                ),
            },
        ),
        (
            "Nacimiento",
            {
                "fields": ("birthdate", "municipality_birth"),
            },
        ),
        (
            "Laboral",
            {
                "fields": (
                    "is_eventual",
                    "weekly_rate",
                    "rfc",
                    "imss",
                    "infonavit",
                    "uniform_date",
                    "status",
                    "status_change_details",
                    "knowledge",
                    "skills",
                    "department",
                ),
            },
        ),
        (
            "Contacto",
            {
                "fields": (
                    "municipality",
                    "neighborhood",
                    "postal_code",
                    "address_street",
                    "address_number",
                    "phone",
                    "emergency_phone",
                ),
            },
        ),
        (
            "Banco",
            {
                "fields": (
                    "bank",
                    "card_number",
                    "balance",
                ),
            },
        ),
        (
            "Otro",
            {
                "fields": (
                    "anti_doping_results",
                    "administrative_violations",
                    "administrative_comments",
                    "status_history",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    # CUSTOM FIELDS
    def custom_links(self, obj):
        """Create custom Imprimir and Ver buttons"""
        return format_html(
            '<a class="btn btn-primary my-1" href="{}" target="_blank">Imprimir</a>'
            "<br />"
            '<a class="btn btn-primary my-1" href="{}">Ver</a>',
            f"/employees/report/employee-details/{obj.id}",
            f"/admin/employees/employee/{obj.id}/preview/",
        )

    # Labels for custom fields
    custom_links.short_description = "Acciones"

    # CUSTOM VIEWS

    def get_urls(self):
        """Setup custom urls"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/preview/",
                self.admin_site.admin_view(self.employee_preview),
                name="employee_preview",
            ),
        ]
        return custom_urls + urls

    def employee_preview(self, request, pk):
        """Custom view to render employee preview"""

        # Check if user has the required permission
        if not request.user.has_perm("employees.view_employee"):
            raise PermissionDenied

        # Get employee
        employee = models.Employee.objects.get(pk=pk)

        # Add specific employee data to the context
        last_name = employee.last_name_1
        if employee.last_name_2:
            last_name += " " + employee.last_name_2
        uniform_date = "N/A"
        if employee.uniform_date:
            uniform_date = employee.uniform_date.strftime("%d/%m/%Y")

        # Get service details
        service = services_models.Service.objects.filter(employee=employee)
        if service:
            service = service[0]
            location = service.location
            company = service.agreement.company_name
            schedule = service.schedule.name
            service_text = f"{company} - {location} ({schedule})"
        else:
            service_text = "N/A"

        # Get admin context
        context = self.admin_site.each_context(request)
        context["employee_data"] = {
            "Nombre": employee.name.title(),
            "Apellidos": last_name.title(),
            "Servicio": service_text,
            "Sueldo": f"$ {employee.weekly_rate} / semana",
            "Fecha de nacimiento": employee.birthdate.strftime("%d/%m/%Y"),
            "Edad": employee.get_age(),
            "RFC": employee.rfc if employee.rfc else "N/A",
            "CURP": employee.curp if employee.curp else "N/A",
            "IMSS": employee.imss if employee.imss else "N/A",
            "Infonavit": employee.infonavit if employee.infonavit else "N/A",
            "Estado Civil": (
                employee.marital_status.name if employee.marital_status else "N/A"
            ),
            "Dirección": f"{employee.address_street} {employee.address_number}".title(),
            "Colonia": employee.neighborhood.name if employee.neighborhood else "N/A",
            "Municipio": employee.municipality.name if employee.municipality else "N/A",
            "C.P.": employee.postal_code,
            "Teléfono": employee.phone,
            "Banco": employee.bank.name if employee.bank else "N/A",
            "Numero de tarjeta": (
                employee.card_number if employee.card_number else "N/A"
            ),
            "Fecha de uniforme": uniform_date,
            "Activo": "Si" if employee.status.name == "Activo" else "No",
            "Historial de estatus": employee.status_history,
        }
        full_name = f"{employee.name.title()} {last_name.title()}"
        context["title"] = f"Vista previa de {full_name}"

        # Render preview
        return render(request, "employees/reports/employee-preview.html", context)


@admin.register(models.Loan)
class Loan(admin.ModelAdmin):
    """WeklyLoan model admin"""

    list_display = (
        "employee",
        "amount",
        "date",
    )
    search_fields = (
        "employee__name",
        "employee__last_name",
        "employee__rfc",
        "employee__curp",
    )
    list_filter = (
        "employee",
        "date",
    )
    list_per_page = 20


@admin.register(models.Ref)
class RefAdmin(admin.ModelAdmin):
    """Ref model admin"""

    list_display = (
        "employee",
        "name",
        "phone",
    )
    search_fields = (
        "employee__name",
        "employee__last_name",
        "employee__rfc",
        "employee__curp",
    )
    list_filter = ("employee",)
    list_per_page = 20


@admin.register(models.Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    """Relationship model admin"""

    list_display = ("name",)


@admin.register(models.Relative)
class RelativeAdmin(admin.ModelAdmin):
    """Relative model admin"""

    list_display = (
        "employee",
        "name",
        "last_name_1",
        "last_name_2",
        "relationship",
    )
    search_fields = (
        "employee__name",
        "employee__last_name",
        "employee__rfc",
        "employee__curp",
    )
    list_filter = (
        "employee",
        "relationship",
    )
    list_per_page = 20
