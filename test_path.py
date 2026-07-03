import os
from django.conf import settings

logo_path = os.path.join(settings.BASE_DIR, 'aplicacion', 'static', 'inicio_sesion', 'img', 'logolecto.png')
print("BASE_DIR:", settings.BASE_DIR)
print("logo_path:", logo_path)
print("Exists:", os.path.exists(logo_path))
