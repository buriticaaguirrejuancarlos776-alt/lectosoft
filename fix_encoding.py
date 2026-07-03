import os
import glob

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = {
        'AtrÃ¡s': 'Atrás',
        'âœ¨': '✨',
        'Â¡DESBLOQUEADO!': '¡DESBLOQUEADO!',
        'TamaÃ±o': 'Tamaño',
        'LIBRERÃ A': 'LIBRERÍA',
        'Ã': 'í',
        'Ã“': 'Ó',
        'Ã¡': 'á',
        'Ã©': 'é',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã±': 'ñ',
        'Â¿': '¿',
        'Â¡': '¡',
        'Ã‘': 'Ñ'
    }
    
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\lectura_dinamica.html')
fix_file(r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\js\lectura_dinamica.js')
print("Fixed encoding in html and js")
