from PIL import Image
logo_path = r"C:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\img\logolecto.png"
with Image.open(logo_path) as img:
    img = img.convert('RGBA')
    colors = img.getcolors(maxcolors=1000000)
    colors.sort(reverse=True)
    for c in colors[:10]:
        print(c)
