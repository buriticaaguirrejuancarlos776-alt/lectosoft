from PIL import Image
logo_path = r"C:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\img\logolecto.png"
with Image.open(logo_path) as img:
    print("Size:", img.size)
