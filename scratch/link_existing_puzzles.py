import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from aplicacion.models import Libro, Rompecabezas

def link_puzzles():
    associations = [
        ('caperucita', 'caperucita'),
        ('principito', 'principito'),
        ('patito', 'patito'),
    ]

    for libro_keyword, puzzle_keyword in associations:
        libro = Libro.objects.filter(titulo__icontains=libro_keyword).first()
        puzzle = Rompecabezas.objects.filter(titulo__icontains=puzzle_keyword, tipo='RETO').first()

        if libro and puzzle:
            puzzle.cuento_asociado = libro
            puzzle.save()
            print(f"Vinculado: {libro.titulo} <-> {puzzle.titulo}")
        else:
            print(f"No se encontró pareja para: {libro_keyword}")

if __name__ == "__main__":
    link_puzzles()
