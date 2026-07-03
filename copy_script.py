import sys
with open(r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\manual_usuario.html', 'r', encoding='utf-8') as f:
    data = f.read()

data = data.replace('Manual de Usuario Lectosoft', 'Manual del Administrador Lectosoft')
data = data.replace('<a href="/" class="btn-volver">⬅ Inicio</a>', '<a href="/administrador/" class="btn-volver">⬅ Panel de Control</a>')
data = data.replace('<title>Lectosoft | Manual de Usuario</title>', '<title>Lectosoft | Manual de Administrador</title>')
data = data.replace('Manual_Usuario_Lectosoft', 'Manual_Administrador_Lectosoft')

with open(r'c:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\templates\manual_admin.html', 'w', encoding='utf-8') as f:
    f.write(data)
