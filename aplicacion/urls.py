from django.urls import path

# pyrefly: ignore [missing-import]
from . import views
# pyrefly: ignore [missing-import]
from . import views_reportes

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.principal, name='principal'),
    path('manual/', views.manual_usuario, name='manual_usuario'),
    path('login/', views.inicio_sesion, name='login'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
    path('menu/', views.menu_juego, name='menu_juego'),
    path('catalogo/', views.catalogos, name='catalogo'),
    path('rompecabeza/', views.rompecabeza, name='rompecabeza'),
    path('trofeo/', views.trofeo, name='trofeo'),
    path('perfil/', views.perfil, name='perfil'),
    path('plata/', views.trofeo_plata, name='plata'),
    path('oro/', views.trofeo_oro, name='oro'),
    path('bronce/', views.trofeo_bronce, name='bronce'),
    path('lectura/', views.lectura, name='lectura'),
    path('lectura1/', views.lectura1, name='lectura1'),
    path('lectura2/', views.lectura2, name='lectura2'),
    
    path('jugadores/', views.admi_usuario, name='admi_usuario'),
    path('eliminar-jugador/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
    path('api/actualizar-nombre-jugador/', views.actualizar_nombre_jugador, name='actualizar_nombre_jugador'),
    path('api/guardar-progreso/', views.guardar_progreso, name='guardar_progreso'),
    
    path('ahorcado/', views.ahorcado, name='ahorcado'),



    path('administrador/', views.administrador, name='administrador'),
    path('administrador/manual/', views.manual_admin, name='manual_admin'),
    path('admi_rompecabeza/', views.admi_rompecabeza, name='admi_rompecabeza'),
    path('admi_rompecabeza/editar/<int:puzzle_id>/', views.admi_rompecabeza, name='preparar_edicion'),
    path('admi_rompecabeza/eliminar/<int:puzzle_id>/', views.eliminar_rompecabeza, name='eliminar_rompecabeza'),
    path('juego_rompecabeza/<int:puzzle_id>/', views.jugar_puzzle, name='jugar_rompecabeza'),
    path('admin_lectura/', views.admin_lectura, name='admin_lectura'),
    path('admin_lectura/editar/<int:libro_id>/', views.admin_lectura, name='preparar_edicion_libro'),
    path('admin_lectura/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('admin_lectura/habilitar/<int:libro_id>/', views.habilitar_libro, name='habilitar_libro'),
    path('admin_lectura/deshabilitar/<int:libro_id>/', views.deshabilitar_libro, name='deshabilitar_libro'),
    path('admin_lectura/generado/<int:libro_id>/', views.admin_editar_libro_generado, name='admin_editar_libro_generado'),
    path('admin_lectura/generado/<int:libro_id>/secciones/', views.admin_editar_secciones, name='admin_editar_secciones'),
    path('admin_lectura/generado/seccion/eliminar/<int:seccion_id>/', views.eliminar_seccion_generada, name='eliminar_seccion_generada'),
    path('admin_lectura/generado/<int:libro_id>/ahorcados/', views.admin_editar_ahorcados, name='admin_editar_ahorcados'),
    path('lectura_dinamica/<slug:slug>/', views.lectura_dinamica, name='lectura_dinamica'),
    # Rutas de Reportes
    path('reportes/', views_reportes.reportes_generales, name='reportes_generales'),
    path('reportes/jugador/<int:jugador_id>/pdf/', views_reportes.reporte_jugador_pdf, name='reporte_jugador_pdf'),
    path('reportes/excel/', views_reportes.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('reportes/pdf/', views_reportes.exportar_reporte_pdf, name='exportar_reporte_pdf'),
    path('reportes/rompecabezas/individual/<int:jugador_id>/', views_reportes.reporte_individual_rompecabezas, name='reporte_individual_rompecabezas'),
    path('reportes/rompecabezas/general/', views_reportes.estadisticas_rompecabezas_admin, name='reportes_rompecabezas_general'),
    path('reportes/rompecabezas/individual/<int:jugador_id>/pdf/', views_reportes.exportar_pdf_rompecabezas_kid, name='exportar_pdf_rompecabezas_kid'),
    
    ]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)