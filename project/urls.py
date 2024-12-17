from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from employees import urls as employees_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('employees/', include(employees_urls)),
]

if not settings.STORAGE_AWS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)