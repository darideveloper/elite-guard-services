from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.urls import include

from employees import urls as employees_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('employees/', include(employees_urls)),
]