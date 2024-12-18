from django.urls import path
from employees import views


urlpatterns = [
    path(
        'report/employee-details/<int:id>/',
        views.ReportEmployeeDetailsView.as_view(),
        name='report-employee'
    ),
]
