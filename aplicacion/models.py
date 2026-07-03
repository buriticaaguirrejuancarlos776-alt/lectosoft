from django.db import models
from django.utils import timezone
import random

def generar_codigo_acceso():
    return str(random.randint(1000, 9999))

class Jugador(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    puntuacion = models.IntegerField(default=0)
    fichas_ganadas = models.IntegerField(default=0)
    codigo_acceso = models.CharField(max_length=4, default=generar_codigo_acceso)
    
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre_usuario

class Rompecabezas(models.Model):
    TIPO_CHOICES = [
        ('RETO', 'Desbloqueo por lectura'),
        ('LIBRE', 'Modo Libre'),
    ]
    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='rompecabezas/')
    dificultad = models.IntegerField(choices=[(3, 'Fácil (3x3)'), (4, 'Medio (4x4)'), (5, 'Difícil (5x5)')], default=3)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='LIBRE')
    cuento_asociado = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True, blank=True, related_name='rompecabezas_retos')

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

class ProgresoJuego(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    rompecabezas = models.ForeignKey(Rompecabezas, on_delete=models.CASCADE)
    paginas_leidas = models.IntegerField(default=0)
    fichas_desbloqueadas = models.IntegerField(default=0)
    puntuacion = models.IntegerField(default=0)
    completado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('jugador', 'rompecabezas')
        verbose_name = "Progreso de Juego"
        verbose_name_plural = "Progresos de Juegos"

    def __str__(self):
        return f"Progreso de {self.jugador.nombre_usuario} en {self.rompecabezas.titulo}"

class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    habilitado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='cuentos/', null=True, blank=True)
    url_lectura = models.CharField(max_length=100)
    es_adicional = models.BooleanField(default=False)
    
    # Nuevos campos para libros generados dinámicamente
    es_generado = models.BooleanField(default=False)
    portada_final = models.ImageField(upload_to='portadas_finales/', null=True, blank=True)
    moraleja = models.TextField(null=True, blank=True, help_text="Moraleja final editable para libros generados.")

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.titulo

class CuentoSeccion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='secciones_generadas')
    orden = models.IntegerField(help_text="Orden de aparición de la sección.")
    texto = models.TextField()
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Sección de Cuento"
        verbose_name_plural = "Secciones de Cuento"
        
    def __str__(self):
        return f"Sección {self.orden} de {self.libro.titulo}"

class AhorcadoPregunta(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='preguntas_ahorcado')
    seccion_activacion = models.IntegerField(help_text="Índice de la sección en la que se activa el ahorcado.")
    pregunta = models.CharField(max_length=255)
    respuesta = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['seccion_activacion']
        verbose_name = "Pregunta de Ahorcado Generado"
        verbose_name_plural = "Preguntas de Ahorcado Generado"
        
    def __str__(self):
        return f"Pregunta en sección {self.seccion_activacion} de {self.libro.titulo}"

class PaginaLibro(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='paginas')
    imagen = models.ImageField(upload_to='paginas_cuentos/')
    numero_pagina = models.IntegerField()
    
    class Meta:
        verbose_name = "Página de Libro"
        verbose_name_plural = "Páginas de Libros"
        ordering = ['numero_pagina']
    def __str__(self):
        return f"Página {self.numero_pagina} de {self.libro.titulo}"

class HistorialLectura(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='historial_lecturas')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    paginas_leidas = models.IntegerField(default=0)
    preguntas_totales = models.IntegerField(default=0)
    preguntas_correctas = models.IntegerField(default=0)
    porcentaje_comprension = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Historial de Lectura"
        verbose_name_plural = "Historiales de Lectura"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.jugador.nombre_usuario} - {self.libro.titulo}"

class HistorialAhorcado(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='historial_ahorcado')
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True, blank=True)
    palabra = models.CharField(max_length=100)
    tiempo_respuesta = models.FloatField(help_text="Tiempo en segundos")
    intentos = models.IntegerField()
    resultado = models.BooleanField(default=False, help_text="True si ganó, False si perdió")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Ahorcado"
        verbose_name_plural = "Historiales de Ahorcado"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.jugador.nombre_usuario} - Ahorcado: {self.palabra}"

class HistorialRompecabezas(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='historial_rompecabezas')
    rompecabezas = models.ForeignKey(Rompecabezas, on_delete=models.CASCADE)
    dificultad = models.IntegerField(choices=[(3, 'Fácil (3x3)'), (4, 'Medio (4x4)'), (5, 'Difícil (5x5)')])
    tiempo_empleado = models.FloatField(help_text="Tiempo en segundos")
    movimientos_correctos = models.IntegerField(default=0, help_text="Piezas colocadas correctamente")
    movimientos_totales = models.IntegerField(default=0, help_text="Total de movimientos realizados")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Rompecabezas"
        verbose_name_plural = "Historiales de Rompecabezas"
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.jugador.nombre_usuario} - Rompecabezas: {self.rompecabezas.titulo}"

class HistorialTrofeo(models.Model):
    TIPO_CHOICES = [
        ('BRONCE', 'Bronce'),
        ('PLATA', 'Plata'),
        ('ORO', 'Oro'),
    ]
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='historial_trofeos')
    tipo_trofeo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Trofeo"
        verbose_name_plural = "Historiales de Trofeos"
        ordering = ['-fecha_obtenida']
        
    def __str__(self):
        return f"{self.jugador.nombre_usuario} - Trofeo {self.get_tipo_trofeo_display()}"