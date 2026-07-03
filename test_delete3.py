import os
import django
from django.conf import settings
from aplicacion.models import Rompecabezas

def test():
    with open('test_output3.txt', 'w') as f:
        puzzles = Rompecabezas.objects.filter(titulo__icontains='soldado')
        for p in puzzles:
            f.write(f"Puzzle ID: {p.id}, Titulo: {p.titulo}, Cuento_asociado: {p.cuento_asociado_id}, Tipo: {p.tipo}\n")

if __name__ == "__main__":
    test()
