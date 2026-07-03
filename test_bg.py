from PIL import Image

logo_path = r"C:\Users\burit\Videos\Lectosoft\proyecto\aplicacion\static\inicio_sesion\img\logolecto.png"
with Image.open(logo_path) as img:
    img = img.convert("RGBA")
    # Create a white background image
    background = Image.new('RGBA', img.size, (255, 255, 255, 255))
    # Paste the image on top of the white background
    background.paste(img, mask=img)
    # Convert to RGB so we drop the alpha channel
    rgb_img = background.convert('RGB')
    rgb_img.save("test_logo_white.png")

print("Saved test_logo_white.png")
