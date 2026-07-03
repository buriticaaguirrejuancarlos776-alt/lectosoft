import os

path = r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\lectura_dinamica.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{{ puzzle.imagen.url }}", "{% if puzzle %}{{ puzzle.imagen.url }}{% endif %}")
content = content.replace("{{ puzzle.dificultad }}", "{% if puzzle %}{{ puzzle.dificultad }}{% else %}3{% endif %}")
content = content.replace("{{ puzzle.id }}", "{% if puzzle %}{{ puzzle.id }}{% endif %}")

old_js = '''            // Páginas dinámicas
            paginasCuento: [
                {% for pagina in paginas_cuento %}
                "{{ pagina.imagen.url }}",
                {% endfor %}
            ]'''

new_js = '''            // Páginas dinámicas
            paginasCuento: (function(){
                var p = [];
                {% for pagina in paginas_cuento %}
                p.push("{% if pagina.imagen %}{{ pagina.imagen.url }}{% endif %}");
                {% endfor %}
                return p;
            })()'''

content = content.replace(old_js, new_js)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML safely")
