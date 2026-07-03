import os
import django
from django.conf import settings
from aplicacion.models import Libro, Rompecabezas

def test():
    with open('test_output.txt', 'w') as f:
        libros = Libro.objects.filter(es_generado=True)
        if not libros:
            f.write("No generated books found.\n")
            return
        libro = libros.first()
        f.write(f"Libro: {libro.titulo}, id: {libro.id}\n")
        
        puzzles = libro.rompecabezas_retos.all()
        f.write(f"Puzzles count from related name: {puzzles.count()}\n")
        for p in puzzles:
            f.write(f" - Puzzle: {p.titulo} (ID: {p.id})\n")
            
        puzzles_query = Rompecabezas.objects.filter(cuento_asociado=libro)
        f.write(f"Puzzles count from query: {puzzles_query.count()}\n")

if __name__ == "__main__":
    test()
