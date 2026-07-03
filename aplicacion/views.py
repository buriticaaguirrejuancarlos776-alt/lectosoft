from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Sum


# pyrefly: ignore [missing-import]
from .models import Rompecabezas, Jugador, ProgresoJuego, Libro, HistorialLectura, HistorialAhorcado, HistorialRompecabezas, HistorialTrofeo, CuentoSeccion, AhorcadoPregunta
from django.contrib import messages
from django.http import JsonResponse
import json
import os
import random
import requests
import urllib.parse
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from functools import wraps
from email.mime.image import MIMEImage
import fitz  # PyMuPDF
import re

# --- Vistas de Navegación ---
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, "Debes iniciar sesión como administrador para acceder a esta área.")
            return redirect('/login/?admin=1')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
def inicio_sesion(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_usuario = request.POST.get('username', '').strip()
        admin_email = request.POST.get('admin_email', '').strip()
        admin_code = request.POST.get('admin_code', '').strip()
        
        # Caso 1: Paso 1 del Administrador (Ingreso de Email)
        if admin_email and not admin_code:
            # RESTRICCIÓN DE SEGURIDAD: Solo un correo permitido
            CORREO_AUTORIZADO = "lectosoft2026@gmail.com"
            
            if admin_email.lower() != CORREO_AUTORIZADO.lower():
                messages.error(request, 'Este correo no está autorizado para acceder como administrador.')
                return render(request, 'inicio_sesion.html')

            # Generar código de seguridad aleatorio
            import random
            from django.core.mail import send_mail
            
            codigo = str(random.randint(100000, 999999))
            request.session['admin_security_code'] = codigo
            request.session['admin_pending_email'] = admin_email
            
            # Intentar enviar el correo HTML profesional
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            from django.conf import settings
            from email.mime.image import MIMEImage
            
            # Datos para la plantilla
            context = {'codigo': codigo}
            html_content = render_to_string('email_codigo.html', context)
            text_content = strip_tags(html_content)
            
            try:
                email = EmailMultiAlternatives(
                    'Código de Seguridad - Lectosoft',
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email]
                )
                email.attach_alternative(html_content, "text/html")
                
                # Adjuntar el logo como imagen incrustada (CID)
                logo_path = os.path.join(settings.BASE_DIR, 'aplicacion', 'static', 'inicio_sesion', 'img', 'logolecto.png')
                if os.path.exists(logo_path):
                    with open(logo_path, 'rb') as f:
                        logo_data = f.read()
                    logo = MIMEImage(logo_data)
                    logo.add_header('Content-ID', '<logolecto>')
                    email.attach(logo)
                
                email.send(fail_silently=False)
            except Exception as e:
                print(f"Error al enviar correo: {e}")
            
            # Simulamos el envío de correo (se muestra en consola para el desarrollador)
            print(f"--- SEGURIDAD LECTOSOFT (HTML ENVIADO) ---")
            print(f"Código para {admin_email}: {codigo}")
            print(f"------------------------------------------")
            
            messages.success(request, f'Se ha enviado un código de seguridad a {admin_email}. Por favor, revise su bandeja de entrada.')
            
            return render(request, 'inicio_sesion.html', {'step': 'code', 'email': admin_email})

        # Caso 2: Paso 2 del Administrador (Verificación de Código)
        if admin_code:
            saved_code = request.session.get('admin_security_code')
            if admin_code == saved_code:
                # Limpiar sesión tras éxito
                del request.session['admin_security_code']
                request.session['is_admin'] = True
                return redirect('administrador')
            else:
                messages.error(request, 'Código de seguridad incorrecto.')
                return render(request, 'inicio_sesion.html', {'step': 'code', 'email': request.session.get('admin_pending_email')})

        # Caso 3: Intento de entrada como Jugador
        # Validar que no esté vacío
        if not nombre_usuario:
            messages.error(request, 'El nombre del jugador no puede estar vacío.')
            return render(request, 'inicio_sesion.html')
        
        # Validar que no sea muy largo
        if len(nombre_usuario) > 100:
            messages.error(request, 'El nombre del jugador es demasiado largo (máximo 100 caracteres).')
            return render(request, 'inicio_sesion.html')
        
        # Obtener el jugador y el código de la petición
        jugador_existente = Jugador.objects.filter(nombre_usuario__iexact=nombre_usuario).first()
        player_code = request.POST.get('player_code', '').strip()
        
        if jugador_existente:
            # Si el jugador existe, debe ingresar su código
            if not player_code:
                return render(request, 'inicio_sesion.html', {'step': 'player_code', 'username': nombre_usuario})
            elif player_code != jugador_existente.codigo_acceso:
                messages.error(request, 'Código incorrecto. Intenta de nuevo.')
                return render(request, 'inicio_sesion.html', {'step': 'player_code', 'username': nombre_usuario})
            else:
                # Todo correcto, iniciar sesión
                response = redirect('/menu/')
                response.set_cookie('jugador_actual', jugador_existente.nombre_usuario, max_age=86400*30)
                return response
        else:
            # Crear el jugador nuevo
            try:
                # El código se autogenera en el modelo por default
                nuevo_jugador = Jugador.objects.create(nombre_usuario=nombre_usuario)
                
                # Renderizar la vista de éxito mostrando el código al niño
                response = render(request, 'inicio_sesion.html', {
                    'step': 'show_code',
                    'username': nombre_usuario,
                    'player_code': nuevo_jugador.codigo_acceso
                })
                # Iniciar sesión en la cookie
                response.set_cookie('jugador_actual', nombre_usuario, max_age=86400*30)
                return response
            except Exception as e:
                messages.error(request, 'Error al registrar el jugador. Intenta nuevamente.')
                return render(request, 'inicio_sesion.html')
    
    return render(request, 'inicio_sesion.html')

def logout_admin(request):
    if 'is_admin' in request.session:
        del request.session['is_admin']
    messages.success(request, "Sesión de administrador cerrada correctamente.")
    return redirect('login')

def menu_juego(request):
    stats = get_jugador_stats(request) if request.COOKIES.get('jugador_actual') else {}
    return render(request, 'menu_juego.html', stats)

def principal(request):
    return render(request, 'principal.html')

def manual_usuario(request):
    pasos_data = [
        {'img': 1, 'texto': 'Pantalla principal de Lectosoft. Desde aquí puedes comenzar tu aventura.'},
        {'img': 2, 'texto': 'Selecciona la opción para iniciar sesión haciendo clic en el botón inferior.'},
        {'img': 3, 'texto': 'Ingresa tu nombre. El sistema te asignará un avatar personalizado automáticamente.'},
        {'img': 4, 'texto': 'Menú principal: Visualiza tus puntos acumulados y elige tu próxima actividad.'},
        {'img': 5, 'texto': 'Sección de Cuentos: Escoge uno de los libros interactivos para empezar a leer.'},
        {'img': 6, 'texto': 'Navega por las páginas del libro mientras disfrutas de la historia.'},
        {'img': 7, 'texto': 'Minijuego del Ahorcado: Aparecerá aleatoriamente para evaluar tu comprensión lectora.'},
        {'img': 8, 'texto': 'Adivina la palabra oculta para ganar fichas valiosas.'},
        {'img': 9, 'texto': '¡Respuesta correcta! Las fichas ganadas te servirán para armar rompecabezas.'},
    ]
    return render(request, 'manual_usuario.html', {'pasos': pasos_data})

@admin_required
def manual_admin(request):
    pasos_data = [
        {'img': 1, 'texto': 'Descripción del paso 1 del panel de administración.'},
        {'img': 2, 'texto': 'Descripción del paso 2 del panel de administración.'},
        {'img': 3, 'texto': 'Descripción del paso 3 del panel de administración.'},
        {'img': 4, 'texto': 'Descripción del paso 4 del panel de administración.'},
        {'img': 5, 'texto': 'Descripción del paso 5 del panel de administración.'},
        {'img': 6, 'texto': 'Descripción del paso 6 del panel de administración.'},
        {'img': 7, 'texto': 'Descripción del paso 7 del panel de administración.'},
        {'img': 8, 'texto': 'Descripción del paso 8 del panel de administración.'},
    ]
    return render(request, 'manual_admin.html', {'pasos': pasos_data})

def catalogos(request):
    libros = Libro.objects.all()
    return render(request, 'catalogos.html', {'libros': libros})

# --- Vistas del Juego ---
def rompecabeza(request):
    puzzles_reto = Rompecabezas.objects.filter(tipo='RETO')
    puzzles_libre = Rompecabezas.objects.filter(tipo='LIBRE')
    return render(request, 'rompecabeza.html', {
        'puzzles_reto': puzzles_reto,
        'puzzles_libre': puzzles_libre
    })

def jugar_puzzle(request, puzzle_id):
    nombre_jugador = request.COOKIES.get('jugador_actual')
    print(f"DEBUG: Accediendo a jugar_puzzle. Jugador en cookie: {nombre_jugador}")
    
    if not nombre_jugador:
        messages.error(request, 'Debes ingresar tu nombre para jugar.')
        return redirect('/')

    puzzle = get_object_or_404(Rompecabezas, id=puzzle_id)
    dificultad = puzzle.dificultad
    grid_size = dificultad * dificultad  # Tamaño de la cuadrícula (3x3 = 9 piezas, 4x4 = 16, 5x5 = 25)

    # Crear las piezas para la cuadrícula según la dificultad
    pieces = []
    for i in range(grid_size):
        x = (i % dificultad) * (450 // dificultad)  # Calcula la posición X de la pieza
        y = (i // dificultad) * (450 // dificultad)  # Calcula la posición Y de la pieza

        pieces.append({
            'index': i,
            'background_position': f"-{x}px -{y}px"
        })

    # Obtener progreso del jugador
    import urllib.parse
    nombre_jugador = request.COOKIES.get('jugador_actual')
    if nombre_jugador:
        nombre_jugador = urllib.parse.unquote(nombre_jugador)
        
    fichas_desbloqueadas = 0
    if str(puzzle.tipo).strip().upper() == 'LIBRE':
        fichas_desbloqueadas = 9999
    elif nombre_jugador:
        jugador = Jugador.objects.filter(nombre_usuario__iexact=nombre_jugador).first()
        if jugador:
            progreso = ProgresoJuego.objects.filter(jugador=jugador, rompecabezas=puzzle).first()
            if progreso:
                fichas_desbloqueadas = progreso.fichas_desbloqueadas
            else:
                fichas_desbloqueadas = 0

    url_lectura = None
    titulo_evaluar = ''
    if puzzle.cuento_asociado:
        titulo_evaluar = puzzle.cuento_asociado.titulo.lower()
    else:
        titulo_evaluar = puzzle.titulo.lower()
        
    if 'caperucita' in titulo_evaluar:
        url_lectura = '/lectura/'
    elif 'patito' in titulo_evaluar:
        url_lectura = '/lectura1/'
    elif 'principito' in titulo_evaluar:
        url_lectura = '/lectura2/'
    else:
        url_lectura = '/lectura/'
            
    # Pasa la dificultad y las piezas a la plantilla
    puzzle_data = {
        'puzzle': puzzle,
        'grid_size': grid_size,
        'dificultad': dificultad,
        'pieces': pieces,
        'fichas_desbloqueadas': fichas_desbloqueadas,
        'url_lectura': url_lectura
    }
    return render(request, 'juego_rompecabeza.html', puzzle_data)

# --- Panel de Administración Unificado (Crear y Editar) ---
@admin_required
def admi_rompecabeza(request, puzzle_id=None):
    puzzle_a_editar = None
    if puzzle_id:
        puzzle_a_editar = get_object_or_404(Rompecabezas, id=puzzle_id)

    error_message = None
    titulo = puzzle_a_editar.titulo if puzzle_a_editar else ''
    dificultad = str(puzzle_a_editar.dificultad) if puzzle_a_editar else '3'
    tipo = puzzle_a_editar.tipo if puzzle_a_editar else 'LIBRE'
    cuento_id = str(puzzle_a_editar.cuento_asociado_id) if puzzle_a_editar and puzzle_a_editar.cuento_asociado_id else ''

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        imagen = request.FILES.get('imagen')
        dificultad = request.POST.get('dificultad', '3')
        tipo = request.POST.get('tipo', puzzle_a_editar.tipo if puzzle_a_editar else 'LIBRE')
        cuento_id = request.POST.get('cuento_asociado', '')

        if imagen:
            filename = imagen.name or ''
            ext = os.path.splitext(filename)[1].lower()
            content_type = imagen.content_type or ''
            if content_type not in ['image/jpeg', 'image/png'] or ext not in ['.jpg', '.jpeg', '.png']:
                error_message = 'Solo se permiten imágenes JPG o PNG. No puede subir PDF, Word u otros formatos.'

        if not error_message and not puzzle_a_editar and not imagen:
            error_message = 'Debe subir una imagen JPG o PNG para crear un rompecabezas.'

        if not error_message and (not titulo or not dificultad):
            error_message = 'Completa todos los campos y sube una imagen JPG o PNG.'

        if not error_message:
            try:
                dificultad_int = int(dificultad)
                if dificultad_int not in [3, 4, 5]:
                    raise ValueError()
            except ValueError:
                error_message = 'La dificultad seleccionada no es válida.'

        if not error_message:
            if puzzle_a_editar:
                puzzle_a_editar.titulo = titulo
                puzzle_a_editar.dificultad = int(dificultad)
                puzzle_a_editar.tipo = tipo
                if cuento_id:
                    puzzle_a_editar.cuento_asociado_id = cuento_id
                else:
                    puzzle_a_editar.cuento_asociado = None
                if imagen:
                    puzzle_a_editar.imagen = imagen
                puzzle_a_editar.save()
            else:
                Rompecabezas.objects.create(
                    titulo=titulo, 
                    imagen=imagen, 
                    dificultad=int(dificultad), 
                    tipo=tipo,
                    cuento_asociado_id=cuento_id if cuento_id else None
                )
            return redirect('admi_rompecabeza')

    libros = Libro.objects.all()
    from django.core.paginator import Paginator
    puzzles_reto_list = Rompecabezas.objects.filter(tipo='RETO').order_by('-id')
    paginator = Paginator(puzzles_reto_list, 8)
    page_number = request.GET.get('page')
    puzzles_reto = paginator.get_page(page_number)
    
    puzzles_libre = Rompecabezas.objects.filter(tipo='LIBRE')
    # Conversión segura para evitar errores de tipo
    try:
        dificultad_int = int(dificultad) if dificultad else 3
    except:
        dificultad_int = 3

    try:
        cuento_id_int = int(cuento_id) if cuento_id else (puzzle_a_editar.cuento_asociado_id if puzzle_a_editar and puzzle_a_editar.cuento_asociado else 0)
    except:
        cuento_id_int = 0

    return render(request, 'admi_rompecabeza.html', {
        'puzzles_reto': puzzles_reto,
        'puzzles_libre': puzzles_libre,
        'puzzle_a_editar': puzzle_a_editar,
        'error_message': error_message,
        'titulo': titulo,
        'dificultad': dificultad_int,
        'tipo': tipo,
        'cuento_id_actual': cuento_id_int,
        'libros': libros,
    })

@csrf_exempt
@admin_required
def eliminar_rompecabeza(request, puzzle_id):
    if request.method == 'POST' or request.method == 'GET':
        try:
            puzzle = get_object_or_404(Rompecabezas, id=puzzle_id)
            if puzzle.imagen:
                puzzle.imagen.delete(save=False)
            puzzle.delete()
            messages.success(request, "Rompecabezas eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar: {str(e)}")
    return redirect('admi_rompecabeza')

# --- Otras Vistas ---
def get_jugador_stats(request):
    nombre_jugador = request.COOKIES.get('jugador_actual')
    if not nombre_jugador:
        return {'puntuacion': 0, 'libros_leidos': 0, 'trofeos_ganados': 0, 'tiene_bronce': False, 'tiene_plata': False, 'tiene_oro': False}
    
    jugador = Jugador.objects.filter(nombre_usuario=nombre_jugador).first()
    if not jugador:
        return {'puntuacion': 0, 'libros_leidos': 0, 'trofeos_ganados': 0, 'tiene_bronce': False, 'tiene_plata': False, 'tiene_oro': False}
    
    libros_leidos = ProgresoJuego.objects.filter(jugador=jugador, paginas_leidas__gt=0).count()
    
    trofeos = 0
    if jugador.puntuacion >= 300: trofeos += 1
    if jugador.puntuacion >= 600: trofeos += 1
    if jugador.puntuacion >= 1000: trofeos += 1
    
    return {
        'puntuacion': jugador.puntuacion,
        'libros_leidos': libros_leidos,
        'trofeos_ganados': trofeos,
        'tiene_bronce': jugador.puntuacion >= 300,
        'tiene_plata': jugador.puntuacion >= 600,
        'tiene_oro': jugador.puntuacion >= 1000,
        'nombre_jugador': nombre_jugador,
        'jugador_id': jugador.id
    }

def trofeo(request):
    return render(request, 'trofeo.html', get_jugador_stats(request))

def perfil(request):
    return render(request, 'perfil.html', get_jugador_stats(request))

def trofeo_bronce(request):
    return render(request, 'trofeo_bronce.html', get_jugador_stats(request))

def trofeo_plata(request):
    return render(request, 'trofeo_plata.html', get_jugador_stats(request))

def trofeo_oro(request):
    return render(request, 'trofeo_oro.html', get_jugador_stats(request))
def lectura(request): 
    nombre_jugador = request.COOKIES.get('jugador_actual')
    print(f"DEBUG: Accediendo a lectura. Jugador en cookie: {nombre_jugador}")
    
    if not nombre_jugador:
        # Si no hay jugador, permitimos ver el cuento sin guardar progreso
        print("DEBUG: Accediendo sin jugador.")

    paginas = 0
    fichas = 0
    
    if nombre_jugador:
        jugador = Jugador.objects.filter(nombre_usuario=nombre_jugador).first()
        if jugador:
            # Buscar el puzzle asociado a este cuento (Caperucita)
            puzzle = Rompecabezas.objects.filter(titulo__icontains="caperucita").first()
            if not puzzle:
                puzzle = Rompecabezas.objects.filter(cuento_asociado__titulo__icontains="caperucita").first()
            if not puzzle:
                puzzle = Rompecabezas.objects.first() # Fallback seguro
                
            if puzzle:
                progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
                paginas = progreso.paginas_leidas
                fichas = progreso.fichas_desbloqueadas
        else:
            puzzle = Rompecabezas.objects.filter(titulo__icontains="caperucita").first() or Rompecabezas.objects.first()
    else:
        puzzle = Rompecabezas.objects.filter(titulo__icontains="caperucita").first() or Rompecabezas.objects.first()
                
    return render(request, 'lectura.html', {
        'paginas_leidas': paginas, 
        'fichas_desbloqueadas': fichas,
        'puzzle': puzzle
    })

def lectura1(request): 
    nombre_jugador = request.COOKIES.get('jugador_actual')
    if not nombre_jugador:
        # Permitir lectura sin jugador
        pass
    
    paginas = 0
    fichas = 0
    jugador = Jugador.objects.filter(nombre_usuario=nombre_jugador).first()
    # Buscar el puzzle asociado a este cuento (Patito Feo)
    puzzle = Rompecabezas.objects.filter(titulo__icontains="patito").first()
    if not puzzle:
        puzzle = Rompecabezas.objects.filter(cuento_asociado__titulo__icontains="patito").first()
    if not puzzle:
        puzzle = Rompecabezas.objects.first()

    if jugador and puzzle:
        progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
        paginas = progreso.paginas_leidas
        fichas = progreso.fichas_desbloqueadas
                
    return render(request, 'lectura1.html', {
        'paginas_leidas': paginas, 
        'fichas_desbloqueadas': fichas,
        'puzzle': puzzle
    })

def lectura2(request): 
    nombre_jugador = request.COOKIES.get('jugador_actual')
    if not nombre_jugador:
        # Permitir lectura sin jugador
        pass
    
    paginas = 0
    fichas = 0
    jugador = Jugador.objects.filter(nombre_usuario=nombre_jugador).first()
    # Buscar el puzzle asociado a este cuento (Principito)
    puzzle = Rompecabezas.objects.filter(titulo__icontains="principito").first()
    if not puzzle:
        puzzle = Rompecabezas.objects.filter(cuento_asociado__titulo__icontains="principito").first()
    if not puzzle:
        puzzle = Rompecabezas.objects.first()

    if jugador and puzzle:
        progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
        paginas = progreso.paginas_leidas
        fichas = progreso.fichas_desbloqueadas
                
    return render(request, 'lectura2.html', {
        'paginas_leidas': paginas, 
        'fichas_desbloqueadas': fichas,
        'puzzle': puzzle
    })


@csrf_exempt
def guardar_progreso(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Priorizamos el nombre que venga en el cuerpo (útil para iframes)
            import urllib.parse
            cookie_nombre = request.COOKIES.get('jugador_actual')
            if cookie_nombre:
                cookie_nombre = urllib.parse.unquote(cookie_nombre)
            
            nombre_jugador = data.get('nombre_jugador') or cookie_nombre
            
            if not nombre_jugador:
                return JsonResponse({'status': 'error', 'message': 'No hay jugador activo'}, status=401)
            print(f"DEBUG: Datos recibidos: {data}")
            
            jugador = Jugador.objects.filter(nombre_usuario__iexact=nombre_jugador).first()
            if not jugador:
                print(f"DEBUG: Jugador {nombre_jugador} no encontrado en DB. Creándolo automáticamente.")
                jugador = Jugador.objects.create(nombre_usuario=nombre_jugador)
            
            # Usamos el puzzle si se especifica y es válido
            puzzle_id = data.get('puzzle_id')
            puzzle = None
            if puzzle_id and str(puzzle_id).lower() not in ['none', 'null', '']:
                try:
                    puzzle = Rompecabezas.objects.get(id=puzzle_id)
                except Rompecabezas.DoesNotExist:
                    puzzle = None

            if puzzle:
                progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
                print(f"DEBUG: Guardando en puzzle {puzzle.id}. Fichas antes: {progreso.fichas_desbloqueadas}")
                
                if 'sumar_fichas' in data:
                    cantidad = int(data['sumar_fichas'])
                    jugador.fichas_ganadas += cantidad
                    progreso.fichas_desbloqueadas += cantidad
                    print(f"DEBUG: Sumando {cantidad} fichas. Total ahora: {progreso.fichas_desbloqueadas}")
                else:
                    print("DEBUG: No vino 'sumar_fichas' en data")
                
                if 'puntuacion' in data:
                    try:
                        delta = int(data['puntuacion'])
                        jugador.puntuacion += delta
                        if jugador.puntuacion < 0:
                            jugador.puntuacion = 0
                        progreso.puntuacion += delta
                        if progreso.puntuacion < 0:
                            progreso.puntuacion = 0
                    except (ValueError, TypeError):
                        print(f"DEBUG: Error al convertir puntuacion: {data.get('puntuacion')}")

                # También actualizamos el objeto progreso por si acaso se usa en otros lados
                paginas_en_data = data.get('paginas_leidas') if 'paginas_leidas' in data else data.get('paginas')
                if paginas_en_data is not None:
                    progreso.paginas_leidas = int(paginas_en_data)
                
            if puzzle:
                progreso.save()
                fichas_ganadas_res = progreso.fichas_desbloqueadas
                puntuacion_res = progreso.puntuacion
            else:
                if 'sumar_fichas' in data:
                    try:
                        cantidad = int(data['sumar_fichas'])
                        jugador.fichas_ganadas += cantidad
                    except (ValueError, TypeError):
                        print(f"DEBUG: Error al sumar fichas sin puzzle: {data.get('sumar_fichas')}")

                if 'puntuacion' in data:
                    try:
                        delta = int(data['puntuacion'])
                        jugador.puntuacion += delta
                        if jugador.puntuacion < 0:
                            jugador.puntuacion = 0
                    except (ValueError, TypeError):
                        print(f"DEBUG: Error al convertir puntuacion: {data.get('puntuacion')}")
                fichas_ganadas_res = jugador.fichas_ganadas
                puntuacion_res = jugador.puntuacion
            
            
            # --- GUARDAR HISTORIALES SI VIENEN EN LOS DATOS ---
            # Inferir libro si hay puzzle
            libro_inferido = None
            if puzzle and hasattr(puzzle, 'cuento_asociado') and puzzle.cuento_asociado:
                libro_inferido = puzzle.cuento_asociado
            
            # Fallback de seguridad por si no hay un cuento_asociado configurado en el administrador
            if not libro_inferido:
                libro_inferido = Libro.objects.first()

            # 1. Historial Lectura
            if 'historial_lectura' in data:
                hl = data['historial_lectura']
                libro_id = hl.get('libro_id')
                libro_obj = Libro.objects.filter(id=libro_id).first() if libro_id else libro_inferido
                if libro_obj:
                    HistorialLectura.objects.create(
                        jugador=jugador,
                        libro=libro_obj,
                        paginas_leidas=hl.get('paginas_leidas', 0),
                        preguntas_totales=hl.get('preguntas_totales', 0),
                        preguntas_correctas=hl.get('preguntas_correctas', 0),
                        porcentaje_comprension=hl.get('porcentaje_comprension', 0.0)
                    )
            
            # 2. Historial Ahorcado
            if 'historial_ahorcado' in data:
                ha = data['historial_ahorcado']
                libro_id = ha.get('libro_id')
                libro_obj = Libro.objects.filter(id=libro_id).first() if libro_id else libro_inferido
                if libro_obj:
                    HistorialAhorcado.objects.create(
                    jugador=jugador,
                    libro=libro_obj,
                    palabra=ha.get('palabra', ''),
                    tiempo_respuesta=ha.get('tiempo_respuesta', 0.0),
                    intentos=ha.get('intentos', 0),
                    resultado=ha.get('resultado', False)
                )

            if 'historial_rompecabezas' in data and puzzle:
                hr = data['historial_rompecabezas']
                HistorialRompecabezas.objects.create(
                    jugador=jugador,
                    rompecabezas=puzzle,
                    dificultad=puzzle.dificultad,
                    tiempo_empleado=hr.get('tiempo_empleado', 0.0),
                    movimientos_correctos=hr.get('movimientos_correctos', 0),
                    movimientos_totales=hr.get('movimientos_totales', 0)
                )

            # 4. Historial Trofeo (Lógica automática básica según puntuación)
            # Revisar si ganó un nuevo trofeo
            if jugador.puntuacion >= 300 and not jugador.historial_trofeos.filter(tipo_trofeo='BRONCE').exists():
                HistorialTrofeo.objects.create(jugador=jugador, tipo_trofeo='BRONCE')
            if jugador.puntuacion >= 600 and not jugador.historial_trofeos.filter(tipo_trofeo='PLATA').exists():
                HistorialTrofeo.objects.create(jugador=jugador, tipo_trofeo='PLATA')
            if jugador.puntuacion >= 1000 and not jugador.historial_trofeos.filter(tipo_trofeo='ORO').exists():
                HistorialTrofeo.objects.create(jugador=jugador, tipo_trofeo='ORO')

            jugador.save()

            return JsonResponse({
                'status': 'success', 
                'fichas': fichas_ganadas_res,
                'puntuacion_total': puntuacion_res
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=400)
@admin_required
def administrador(request): return render(request, 'administrador.html')
@xframe_options_exempt
def ahorcado(request):
    import urllib.parse
    nombre_jugador = request.COOKIES.get('jugador_actual')
    if nombre_jugador:
        nombre_jugador = urllib.parse.unquote(nombre_jugador)
        
    puntos = 0
    fichas = 0
    if nombre_jugador:
        jugador = Jugador.objects.filter(nombre_usuario__iexact=nombre_jugador).first()
        if jugador:
            puzzle_id = request.GET.get('puzzle')
            puzzle = None
            if puzzle_id and str(puzzle_id).lower() not in ['none', 'null', '']:
                try:
                    puzzle = Rompecabezas.objects.get(id=puzzle_id)
                except Rompecabezas.DoesNotExist:
                    puzzle = None
            
            if not puzzle:
                puzzle = Rompecabezas.objects.first()
                
            if puzzle:
                progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
                puntos = progreso.puntuacion
                fichas = progreso.fichas_desbloqueadas
            else:
                puntos = jugador.puntuacion
                fichas = jugador.fichas_ganadas
    return render(request, 'ahorcado.html', {
        'puntos': puntos, 
        'fichas': fichas,
        'nombre_jugador': nombre_jugador
    })

@admin_required
def admi_usuario(request):
    from django.core.paginator import Paginator
    usuarios_list = Jugador.objects.all().order_by('-fecha_creacion')
    total_puntos = Jugador.objects.aggregate(Sum('puntuacion'))['puntuacion__sum'] or 0
    
    paginator = Paginator(usuarios_list, 6)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    
    return render(request, 'admi_usuario.html', {
        'usuarios': usuarios,
        'total_puntos': total_puntos
    })

@csrf_exempt
@admin_required
def eliminar_jugador(request, jugador_id):
    if request.method == 'POST' or request.method == 'GET':
        try:
            jugador = get_object_or_404(Jugador, id=jugador_id)
            nombre = jugador.nombre_usuario
            jugador.delete()
            messages.success(request, f"Jugador '{nombre}' eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar jugador: {str(e)}")
    return redirect('admi_usuario')

@csrf_exempt
def actualizar_nombre_jugador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_anterior = data.get('nombre_anterior', '').strip()
            nombre_nuevo = data.get('nombre_nuevo', '').strip()
            
            if not nombre_anterior or not nombre_nuevo:
                return JsonResponse({'status': 'error', 'message': 'Nombres requeridos'}, status=400)
            
            # Verificar que no exista otro jugador con el nuevo nombre
            jugador_existente = Jugador.objects.filter(nombre_usuario__iexact=nombre_nuevo).exclude(nombre_usuario__iexact=nombre_anterior)
            if jugador_existente.exists():
                return JsonResponse({'status': 'error', 'message': 'Nombre ya en uso'}, status=400)
            
            # Actualizar el nombre
            jugador = Jugador.objects.get(nombre_usuario__iexact=nombre_anterior)
            jugador.nombre_usuario = nombre_nuevo
            jugador.save()
            
            response = JsonResponse({'status': 'success', 'message': 'Nombre actualizado'})
            response.set_cookie('jugador_actual', urllib.parse.quote(nombre_nuevo), max_age=31536000, path='/')
            return response
        except Jugador.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Jugador no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Datos inválidos'}, status=400)
        except Exception as e:
            print(f'Error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
@admin_required
def admin_lectura(request, libro_id=None):
    libro_a_editar = None
    if libro_id:
        libro_a_editar = get_object_or_404(Libro, id=libro_id)

    if request.method == 'GET' and request.GET.get('accion') == 'importar_openlibrary':
        titulo = request.GET.get('titulo')
        url_lectura = request.GET.get('url_lectura')
        imagen_url = request.GET.get('imagen_url')
        
        if Libro.objects.filter(titulo__iexact=titulo).exists():
            messages.error(request, f"El libro '{titulo}' ya está en tu catálogo.")
            return redirect('admin_lectura')
        
        titulo_seguro = titulo[:149]
        slug = slugify(titulo)[:40] or 'openlibrary-book'
        if Libro.objects.filter(slug=slug).exists():
            slug += str(random.randint(1000, 9999))
            
        libro = Libro.objects.create(
            titulo=titulo_seguro,
            slug=slug,
            url_lectura=url_lectura,
            es_adicional=True
        )
        
        if imagen_url and imagen_url != 'None':
            try:
                response = requests.get(imagen_url, timeout=10)
                if response.status_code == 200:
                    libro.imagen.save(f"ol_{slug}.jpg", ContentFile(response.content), save=True)
            except Exception as e:
                pass
                
        messages.success(request, f"El libro '{titulo}' se ha importado desde Open Library.")
        return redirect('admin_lectura')

    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            titulo = request.POST.get('titulo', 'Nuevo Cuento').strip()
            
            # Validación de duplicados
            if Libro.objects.filter(titulo__iexact=titulo).exists():
                messages.error(request, f"El cuento '{titulo}' ya existe en el catálogo. Por favor, usa un título diferente.")
                return redirect('admin_lectura')

            imagen = request.FILES.get('imagen')
            url_lectura = request.POST.get('url_lectura', '/lectura/')
            
            if imagen:
                slug = slugify(titulo) or 'cuento'
                if Libro.objects.filter(slug=slug).exists():
                    slug += str(random.randint(1000, 9999))
                
                libro = Libro.objects.create(
                    titulo=titulo,
                    slug=slug,
                    imagen=imagen,
                    url_lectura=url_lectura,
                    es_adicional=False
                )
                
                # Crear Rompecabezas asociado automáticamente
                Rompecabezas.objects.create(
                    titulo=f"Rompecabezas de {titulo}",
                    imagen=libro.imagen,
                    dificultad=3,
                    tipo='RETO',
                    cuento_asociado=libro
                )
                
                messages.success(request, f"Cuento '{titulo}' creado correctamente.")
            else:
                messages.error(request, "Debe seleccionar una imagen para el cuento.")
            return redirect('admin_lectura')

        elif accion == 'importar_openlibrary':
            titulo = request.POST.get('titulo')
            url_lectura = request.POST.get('url_lectura')
            imagen_url = request.POST.get('imagen_url')
            
            if Libro.objects.filter(titulo__iexact=titulo).exists():
                messages.error(request, f"El libro '{titulo}' ya está en tu catálogo.")
                return redirect('admin_lectura')
            
            # Asegurar límites de base de datos
            titulo_seguro = titulo[:149]
            slug = slugify(titulo)[:40] or 'openlibrary-book'
            if Libro.objects.filter(slug=slug).exists():
                slug += str(random.randint(1000, 9999))
                
            libro = Libro.objects.create(
                titulo=titulo_seguro,
                slug=slug,
                url_lectura=url_lectura,
                es_adicional=True # Lo usamos para identificar que es de Open Library
            )
            
            # Descargar imagen
            if imagen_url and imagen_url != 'None':
                try:
                    response = requests.get(imagen_url, timeout=10)
                    if response.status_code == 200:
                        libro.imagen.save(f"ol_{slug}.jpg", ContentFile(response.content), save=True)
                except Exception as e:
                    print(f"Error descargando imagen: {e}")
                    
            if libro.imagen:
                # Crear Rompecabezas asociado automáticamente
                Rompecabezas.objects.create(
                    titulo=f"Rompecabezas de {titulo_seguro}",
                    imagen=libro.imagen,
                    dificultad=3,
                    tipo='RETO',
                    cuento_asociado=libro
                )
                    
            messages.success(request, f"El libro '{titulo}' se ha importado desde Google Books.")
            return redirect('admin_lectura')

        elif accion == 'generar_pdf':
            titulo = request.POST.get('titulo', 'Libro Generado').strip()
            archivo_pdf = request.FILES.get('archivo_pdf')
            imagen_portada = request.FILES.get('imagen_portada')
            
            if not archivo_pdf:
                messages.error(request, "Debe seleccionar un archivo PDF.")
                return redirect('admin_lectura')
                
            slug = slugify(titulo) or 'generado'
            if Libro.objects.filter(slug=slug).exists():
                slug += f"-{random.randint(1000, 9999)}"
                
            # Crear Libro
            libro = Libro.objects.create(
                titulo=titulo,
                slug=slug,
                url_lectura=f'/lectura_dinamica/{slug}/',
                es_generado=True,
                moraleja="Añade aquí tu moraleja."
            )
            
            if imagen_portada:
                libro.imagen = imagen_portada
                libro.save()
            
            try:
                # Extraer PDF con PyMuPDF
                pdf_document = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
                texto_completo = ""
                
                # Extraer portada inicial (primera página) si no hay imagen_portada
                if not imagen_portada and len(pdf_document) > 0:
                    page = pdf_document.load_page(0)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Alta resolución
                    img_data = pix.tobytes("png")
                    libro.imagen.save(f"portada_{slug}.png", ContentFile(img_data), save=True)
                
                # Extraer portada final (última página)
                if len(pdf_document) > 1:
                    page = pdf_document.load_page(len(pdf_document)-1)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = pix.tobytes("png")
                    libro.portada_final.save(f"portada_fin_{slug}.png", ContentFile(img_data), save=True)
                
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    texto_completo += page.get_text() + " "
                
                # Limpiar texto
                texto_completo = re.sub(r'\s+', ' ', texto_completo).strip()
                
                # Si el PDF no tenía texto
                if not texto_completo:
                    texto_completo = "El PDF no contiene texto extraíble."
                
                # Dividir texto en secciones (ej: cada 250 caracteres aprox)
                palabras = texto_completo.split()
                secciones = []
                seccion_actual = ""
                for palabra in palabras:
                    seccion_actual += palabra + " "
                    if len(seccion_actual) > 250:
                        secciones.append(seccion_actual.strip())
                        seccion_actual = ""
                if seccion_actual:
                    secciones.append(seccion_actual.strip())
                
                # Si es muy corto
                if len(secciones) == 0:
                    secciones.append(texto_completo)
                
                # Crear CuentoSeccion
                for index, texto_secc in enumerate(secciones):
                    CuentoSeccion.objects.create(libro=libro, orden=index, texto=texto_secc)
                    
                    # Generar ahorcado cada 10 secciones
                    if index > 0 and (index + 1) % 10 == 0:
                        # Seleccionar la palabra más larga como "respuesta" genérica
                        pals_seccion = [re.sub(r'[^A-Za-zñÑáéíóúÁÉÍÓÚ]', '', p) for p in texto_secc.split()]
                        pals_seccion = [p for p in pals_seccion if len(p) > 4]
                        respuesta = random.choice(pals_seccion).upper() if pals_seccion else "PALABRA"
                        AhorcadoPregunta.objects.create(
                            libro=libro,
                            seccion_activacion=index,
                            pregunta=f"Encuentra la palabra oculta relacionada con la lectura.",
                            respuesta=respuesta
                        )
                
                # Crear Rompecabezas asociado automáticamente
                Rompecabezas.objects.create(
                    titulo=f"Rompecabezas de {titulo}",
                    imagen=libro.imagen if libro.imagen else None,
                    dificultad=3,
                    tipo='RETO',
                    cuento_asociado=libro
                )
                
                messages.success(request, f"Libro interactivo '{titulo}' generado correctamente desde PDF.")
            except Exception as e:
                libro.delete()
                messages.error(request, f"Error al procesar el PDF: {str(e)}")
            
            return redirect('admin_lectura')

        elif accion == 'actualizar_imagen':
            id_final = request.POST.get('libro_id') or libro_id
            libro = get_object_or_404(Libro, id=id_final)
            nueva_imagen = request.FILES.get('imagen')
            url_lectura = request.POST.get('url_lectura')
            
            if nueva_imagen:
                libro.imagen = nueva_imagen
            if url_lectura:
                libro.url_lectura = url_lectura
            libro.save()
            messages.success(request, f"Cuento '{libro.titulo}' actualizado.")
            return redirect('admin_lectura')

    libros_clasicos = Libro.objects.filter(es_adicional=False, es_generado=False).order_by('id')
    libros_openlibrary = Libro.objects.filter(es_adicional=True, es_generado=False).order_by('id')
    
    from django.core.paginator import Paginator
    libros_generados_list = Libro.objects.filter(es_generado=True).order_by('-id')
    paginator = Paginator(libros_generados_list, 3)
    page_number = request.GET.get('page')
    libros_generados = paginator.get_page(page_number)
    
    # Preparar datos para el formulario (edición o nuevo)
    url_lectura_actual = libro_a_editar.url_lectura if libro_a_editar else ''
    
    return render(request, 'admin_lectura.html', {
        'libros_clasicos': libros_clasicos,
        'libros_openlibrary': libros_openlibrary,
        'libros_generados': libros_generados,
        'libro_a_editar': libro_a_editar,
        'url_lectura_actual': url_lectura_actual,
    })

@admin_required
def habilitar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    libro.habilitado = True
    libro.save()
    messages.success(request, f"Cuento '{libro.titulo}' habilitado.")
    return redirect('admin_lectura')

@admin_required
def deshabilitar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    libro.habilitado = False
    libro.save()
    messages.success(request, f"Cuento '{libro.titulo}' deshabilitado.")
    return redirect('admin_lectura')

@csrf_exempt
@admin_required
def eliminar_libro(request, libro_id):
    if request.method == 'POST' or request.method == 'GET':
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            titulo = libro.titulo
            
            # Eliminar rompecabezas asociados y sus imágenes
            for rompecabeza in libro.rompecabezas_retos.all():
                if rompecabeza.imagen:
                    try:
                        rompecabeza.imagen.delete(save=False)
                    except Exception:
                        pass
                rompecabeza.delete()

            # También eliminar rompecabezas huérfanos que tengan el título de este libro
            huerfanos = Rompecabezas.objects.filter(cuento_asociado__isnull=True, titulo__icontains=titulo)
            for rompecabeza in huerfanos:
                if rompecabeza.imagen:
                    try:
                        rompecabeza.imagen.delete(save=False)
                    except Exception:
                        pass
                rompecabeza.delete()

            if libro.imagen:
                try:
                    libro.imagen.delete(save=False)
                except Exception:
                    pass
            if libro.es_adicional:
                for pagina in libro.paginas.all():
                    if pagina.imagen:
                        try:
                            pagina.imagen.delete(save=False)
                        except Exception:
                            pass
            libro.delete()
            messages.success(request, f"El cuento '{titulo}' ha sido eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al intentar eliminar el cuento: {str(e)}")
    return redirect('admin_lectura')

# --- VISTAS LIBROS GENERADOS DINÁMICAMENTE ---
@admin_required
def admin_editar_libro_generado(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id, es_generado=True)
    if request.method == 'POST':
        moraleja = request.POST.get('moraleja')
        if moraleja is not None:
            libro.moraleja = moraleja
            libro.save()
            messages.success(request, "Moraleja actualizada.")
        return redirect('admin_editar_libro_generado', libro_id=libro.id)
        
    secciones = libro.secciones_generadas.all().order_by('orden')
    ahorcados = libro.preguntas_ahorcado.all().order_by('seccion_activacion')
    return render(request, 'admin_editar_libro.html', {
        'libro': libro,
        'secciones': secciones,
        'ahorcados': ahorcados
    })

@admin_required
def admin_editar_secciones(request, libro_id):
    from django.core.paginator import Paginator
    from django.urls import reverse
    libro = get_object_or_404(Libro, id=libro_id, es_generado=True)
    
    if request.method == 'POST':
        for seccion in libro.secciones_generadas.all():
            texto = request.POST.get(f'texto_{seccion.id}')
            if texto is not None:
                seccion.texto = texto
                seccion.save()
        messages.success(request, "Secciones actualizadas.")
        page_number = request.POST.get('page', '1')
        url = reverse('admin_editar_secciones', args=[libro.id])
        return redirect(f"{url}?page={page_number}")
        
    secciones_list = libro.secciones_generadas.all().order_by('orden')
    paginator = Paginator(secciones_list, 5) # 5 secciones por página
    page_number = request.GET.get('page')
    secciones = paginator.get_page(page_number)
    
    return render(request, 'admin_editar_secciones.html', {'libro': libro, 'secciones': secciones})

@csrf_exempt
@admin_required
def eliminar_seccion_generada(request, seccion_id):
    if request.method == 'POST':
        seccion = get_object_or_404(CuentoSeccion, id=seccion_id)
        libro = seccion.libro
        seccion_orden_borrada = seccion.orden
        seccion.delete()
        
        from django.db.models import F

        # Reordenar las secciones restantes masivamente
        libro.secciones_generadas.filter(orden__gt=seccion_orden_borrada).update(orden=F('orden') - 1)
            
        # Ajustar los ahorcados para que apunten a la sección correcta
        libro.preguntas_ahorcado.filter(seccion_activacion__gt=seccion_orden_borrada).update(seccion_activacion=F('seccion_activacion') - 1)
        # Si estaba en la sección borrada, lo movemos a la anterior (si es > 0)
        libro.preguntas_ahorcado.filter(seccion_activacion=seccion_orden_borrada, seccion_activacion__gt=0).update(seccion_activacion=F('seccion_activacion') - 1)
            
        messages.success(request, "Sección eliminada exitosamente y secciones/ahorcados reorganizados.")
        return redirect('admin_editar_secciones', libro_id=libro.id)
    return redirect('admin_lectura')

@admin_required
def admin_editar_ahorcados(request, libro_id):
    from django.core.paginator import Paginator
    from django.urls import reverse
    libro = get_object_or_404(Libro, id=libro_id, es_generado=True)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'agregar':
            pregunta = request.POST.get('nueva_pregunta', '').strip()
            respuesta = request.POST.get('nueva_respuesta', '').strip()
            seccion = request.POST.get('nueva_seccion')
            if pregunta and respuesta and seccion:
                try:
                    AhorcadoPregunta.objects.create(
                        libro=libro,
                        seccion_activacion=int(seccion),
                        pregunta=pregunta,
                        respuesta=respuesta.upper()
                    )
                    messages.success(request, "Nueva pregunta de ahorcado agregada exitosamente.")
                except Exception as e:
                    messages.error(request, f"Error al agregar: {str(e)}")
            else:
                messages.error(request, "Debe llenar todos los campos para agregar un ahorcado.")
                
        elif accion == 'eliminar':
            pregunta_id = request.POST.get('pregunta_id')
            if pregunta_id:
                try:
                    p = AhorcadoPregunta.objects.get(id=pregunta_id, libro=libro)
                    p.delete()
                    messages.success(request, "Pregunta eliminada exitosamente.")
                except AhorcadoPregunta.DoesNotExist:
                    messages.error(request, "La pregunta no existe.")
                    
        else:
            # Edición masiva de las existentes
            for pregunta in libro.preguntas_ahorcado.all():
                preg = request.POST.get(f'pregunta_{pregunta.id}')
                resp = request.POST.get(f'respuesta_{pregunta.id}')
                if preg and resp:
                    pregunta.pregunta = preg
                    pregunta.respuesta = resp.upper()
                    pregunta.save()
            messages.success(request, "Preguntas de ahorcado actualizadas.")
            
        page_number = request.POST.get('page', '1')
        url = reverse('admin_editar_ahorcados', args=[libro.id])
        return redirect(f"{url}?page={page_number}")
        
    ahorcados_list = libro.preguntas_ahorcado.all().order_by('seccion_activacion')
    paginator = Paginator(ahorcados_list, 5) # 5 ahorcados por página
    page_number = request.GET.get('page')
    ahorcados = paginator.get_page(page_number)

    secciones = libro.secciones_generadas.all().order_by('orden')
    return render(request, 'admin_editar_ahorcados.html', {
        'libro': libro, 
        'ahorcados': ahorcados,
        'secciones': secciones
    })

def lectura_dinamica(request, slug):
    nombre_jugador = request.COOKIES.get('jugador_actual')
    libro = get_object_or_404(Libro, slug=slug, es_generado=True)
    
    paginas = 0
    fichas = 0
    
    # Buscar puzzle asociado
    puzzle = Rompecabezas.objects.filter(cuento_asociado=libro).first()
    
    # Si el libro no tiene un rompecabezas asociado (por ser antiguo o importado antes), lo creamos al vuelo
    if not puzzle and libro.imagen:
        try:
            puzzle = Rompecabezas.objects.create(
                titulo=f"Rompecabezas de {libro.titulo}",
                imagen=libro.imagen,
                dificultad=3,
                tipo='RETO',
                cuento_asociado=libro
            )
        except Exception as e:
            print(f"DEBUG: No se pudo auto-crear el puzzle para {libro.titulo}: {e}")
            puzzle = None
    
    if nombre_jugador:
        jugador = Jugador.objects.filter(nombre_usuario=nombre_jugador).first()
        if jugador and puzzle:
            progreso, _ = ProgresoJuego.objects.get_or_create(jugador=jugador, rompecabezas=puzzle)
            paginas = progreso.paginas_leidas
            fichas = progreso.fichas_desbloqueadas

    # Preparar datos JSON para JS
    secciones = list(libro.secciones_generadas.all().order_by('orden').values('orden', 'texto'))
    ahorcados = list(libro.preguntas_ahorcado.all().order_by('seccion_activacion').values('seccion_activacion', 'pregunta', 'respuesta'))
    
    libro_data = {
        'titulo': libro.titulo,
        'portada_url': libro.imagen.url if libro.imagen else '',
        'portada_fin_url': libro.portada_final.url if libro.portada_final else '',
        'moraleja': libro.moraleja,
        'secciones': secciones,
        'ahorcados': ahorcados
    }

    return render(request, 'lectura_dinamica.html', {
        'paginas_leidas': paginas, 
        'fichas_desbloqueadas': fichas,
        'puzzle': puzzle,
        'libro': libro,
        'libro_data': json.dumps(libro_data)
    })