import re

html_path = r"c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\ahorcado.html"
css_path = r"c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\css\ahorcado.css"
js_path = r"c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\js\ahorcado.js"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if css_match:
    css_content = css_match.group(1).strip()
    
    css_content = re.sub(r'"\{% static \'inicio_sesion/img/(.*?)\' %\}"', r'"../img/\1"', css_content)
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)

script_matches = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
if script_matches:
    js_content = "\n\n".join(match.strip() for match in script_matches)
    
    js_content = js_content.replace('Number("{{ puntos|default:0 }}")', 'window.gameConfig.puntos')
    js_content = js_content.replace('Number("{{ fichas|default:0 }}")', 'window.gameConfig.fichas')
    js_content = js_content.replace('"{{ nombre_jugador|default:\'\' }}"', 'window.gameConfig.nombreJugador')
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

# Update HTML
if css_match and script_matches:
    new_html = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="{% static \'inicio_sesion/css/ahorcado.css\' %}">', content, flags=re.DOTALL)
    
    config_script = '''<script>
        window.gameConfig = {
            puntos: Number("{{ puntos|default:0 }}") || 0,
            fichas: Number("{{ fichas|default:0 }}") || 0,
            nombreJugador: "{{ nombre_jugador|default:'' }}"
        };
    </script>
    <script src="{% static 'inicio_sesion/js/ahorcado.js' %}"></script>'''
    
    parts = re.split(r'<script>.*?</script>', new_html, flags=re.DOTALL)
    if len(parts) == 3:
        final_html = parts[0] + config_script + parts[1] + parts[2]
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("Success")
    else:
        print("Error splitting script tags")
else:
    print("Could not find style or script tags")
