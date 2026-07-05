# Lectosoft

Aplicación web educativa en Django para fomentar la lectura infantil: los
niños leen cuentos interactivos y desbloquean minijuegos (rompecabezas y
ahorcado) a medida que avanzan. Incluye un panel de administración para
gestionar cuentos, rompecabezas, jugadores y reportes de progreso.

## Funcionalidad

- **Cuentos interactivos**: lectura página por página, incluyendo cuentos
  generados dinámicamente con secciones y moraleja editables.
- **Minijuegos ligados a la lectura**: rompecabezas (3x3 a 5x5) y ahorcado
  que se desbloquean como "retos" al avanzar en la lectura, o en modo libre.
- **Progreso y logros**: puntuación, fichas ganadas y trofeos (bronce/plata/oro)
  por jugador.
- **Panel de administración** (`/administrador/`): CRUD de cuentos, páginas,
  rompecabezas y jugadores; habilitar/deshabilitar cuentos.
- **Reportes**: estadísticas generales y por jugador, exportables a PDF
  (ReportLab) y Excel (openpyxl).

## Stack

- Django 6.0 (`proyecto/`), app principal `aplicacion/`
- MySQL (`mysqlclient`)
- WhiteNoise para archivos estáticos en producción
- Gunicorn como servidor WSGI

## Desarrollo local

1. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copiar `.env.example` a `.env` y ajustar los valores (o dejar los de
   desarrollo local si ya tienes MySQL corriendo en `localhost`):
   ```bash
   cp .env.example .env
   ```
3. Crear la base de datos MySQL (`DB_NAME` del `.env`) y aplicar migraciones:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Levantar el servidor:
   ```bash
   python manage.py runserver
   ```

## Despliegue

Corre containerizado (Docker + `docker-compose`) detrás de Caddy, en el mismo
servidor Hetzner que otros proyectos, compartiendo un único Caddy externo por
red Docker (`caddy_net`). El despliegue a producción es automático: cada push
a `main` dispara `.github/workflows/deploy.yml`, que hace backup de la base de
datos (`mysqldump`) y luego `docker compose up -d --build` en el servidor
(ver `scripts/deploy.sh`).

Detalles de acceso al servidor, arquitectura de Caddy y credenciales están en
un documento aparte (no versionado en este repo) que maneja quien administra
el despliegue.

## Estructura

```
proyecto/       # settings, urls, wsgi/asgi del proyecto Django
aplicacion/     # app principal: modelos, vistas, templates, estáticos
  migrations/
  static/
  templates/
scripts/deploy.sh              # script de despliegue (con backup de BD)
.github/workflows/deploy.yml   # CI/CD: despliega en push a main
Dockerfile / docker-compose.yml
```

> Despliegue automático verificado (llave SSH dedicada renovada) el 2026-07-05.
