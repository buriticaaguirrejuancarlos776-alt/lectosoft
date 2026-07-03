import re

path = r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\lectura_dinamica.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_js = '''            // Páginas dinámicas
            paginasCuento: JSON.parse(document.getElementById('paginas-data').textContent)'''

content = re.sub(r'            // Páginas dinámicas\s*paginasCuento: \(function\(\)\{[\s\S]*?\}\)\(\)', new_js, content)

content = content.replace('<script>', '{{ paginas_urls|json_script:"paginas-data" }}\n    <script>', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated HTML successfully')
