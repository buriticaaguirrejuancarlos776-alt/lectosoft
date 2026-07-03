import os
import django
from django.conf import settings
from aplicacion.models import Rompecabezas

def test():
    with open('test_output4.txt', 'w') as f:
        puzzles = Rompecabezas.objects.all()
        for p in puzzles:
            f.write(f"ID: {p.id}, Titulo: {p.titulo}, Cuento: {p.cuento_asociado_id}, Tipo: {p.tipo}\n")

if __name__ == "__main__":
    test()
