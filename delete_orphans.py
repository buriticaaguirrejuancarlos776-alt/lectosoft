import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from aplicacion.models import Libro, Rompecabezas, PaginaLibro
from django.conf import settings

media_root = settings.MEDIA_ROOT

def delete_orphans(directory_name, db_images_list):
    dir_path = os.path.join(media_root, directory_name)
    if not os.path.exists(dir_path):
        return

    # Archivos físicos en la carpeta
    physical_files = set(f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))
    
    # Nombres de archivo de la BD
    db_files = set()
    for img_path in db_images_list:
        if img_path:
            db_files.add(os.path.basename(img_path))

    orphans = physical_files - db_files
    
    deleted_count = 0
    for f in orphans:
        try:
            os.remove(os.path.join(dir_path, f))
            deleted_count += 1
        except Exception as e:
            print(f"Error borrando {f}: {e}")
            
    print(f"[{directory_name}] Se eliminaron {deleted_count} archivos huérfanos.")

print("Iniciando eliminación de imágenes huérfanas...")

# 1. portadas_finales (Libro.portada_final)
portadas_db = list(Libro.objects.exclude(portada_final__isnull=True).exclude(portada_final__exact='').values_list('portada_final', flat=True))
delete_orphans('portadas_finales', portadas_db)

# 2. rompecabezas (Rompecabezas.imagen)
rompecabezas_db = list(Rompecabezas.objects.exclude(imagen__isnull=True).exclude(imagen__exact='').values_list('imagen', flat=True))
delete_orphans('rompecabezas', rompecabezas_db)

# 3. cuentos (Libro.imagen)
cuentos_db = list(Libro.objects.exclude(imagen__isnull=True).exclude(imagen__exact='').values_list('imagen', flat=True))
delete_orphans('cuentos', cuentos_db)

# 4. paginas_cuentos (PaginaLibro.imagen)
paginas_db = list(PaginaLibro.objects.exclude(imagen__isnull=True).exclude(imagen__exact='').values_list('imagen', flat=True))
delete_orphans('paginas_cuentos', paginas_db)

print("Proceso completado.")
