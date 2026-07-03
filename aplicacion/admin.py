from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Jugador, Rompecabezas

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'puntuacion', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre_usuario',)
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)

@admin.register(Rompecabezas)
class RompecabezasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'dificultad')
    list_filter = ('dificultad',)
    search_fields = ('titulo',)
