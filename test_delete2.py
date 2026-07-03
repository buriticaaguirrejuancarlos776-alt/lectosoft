import os
import django
from django.conf import settings
from aplicacion.models import Libro, Rompecabezas

def test():
    with open('test_output2.txt', 'w') as f:
        libros = Libro.objects.filter(es_generado=True)
        if not libros:
            f.write("No generated books found.\n")
            return
        libro = libros.first()
        f.write(f"Deleting Libro: {libro.titulo}, id: {libro.id}\n")
        
        # Copied from views.eliminar_libro
        for rompecabeza in libro.rompecabezas_retos.all():
            f.write(f"Deleting Puzzle: {rompecabeza.titulo} (ID: {rompecabeza.id})\n")
            if rompecabeza.imagen:
                try:
                    rompecabeza.imagen.delete(save=False)
                    f.write(" - Deleted image\n")
                except Exception as e:
                    f.write(f" - Error deleting image: {e}\n")
            rompecabeza.delete()
            f.write(" - Deleted puzzle from DB\n")
            
        if libro.imagen:
            try:
                libro.imagen.delete(save=False)
                f.write(" - Deleted book image\n")
            except Exception as e:
                f.write(f" - Error deleting book image: {e}\n")
        
        # Check puzzles after deletion
        puzzles_query = Rompecabezas.objects.filter(cuento_asociado_id=libro.id)
        f.write(f"Puzzles count after rompecabeza.delete(): {puzzles_query.count()}\n")

        libro.delete()
        f.write(" - Deleted book from DB\n")
        
        puzzles_total = Rompecabezas.objects.filter(titulo__icontains=libro.titulo).count()
        f.write(f"Puzzles with similar title after book deletion: {puzzles_total}\n")

if __name__ == "__main__":
    test()
