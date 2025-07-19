import os

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # Delete employees/temp_qr_images folder when project starts
        qr_images_path = os.path.join(settings.BASE_DIR, "employees", "temp_qr_images")
        if os.path.exists(qr_images_path):
            # Delete folder contents
            for file_name in os.listdir(qr_images_path):
                file_path = os.path.join(qr_images_path, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error: {e}")
