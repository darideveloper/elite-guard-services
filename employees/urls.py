from django.urls import path
from employees import views


urlpatterns = [
    path(
        'report/employee/<int:id>',
        views.ReportEmployeeView.as_view(),
        name='report-employee'
    ),
]
