# Guía de despliegue en una VPS con Docker

Esta guía es genérica: aplica en cualquier VPS con Ubuntu 22.04/24.04 y
Docker. Este proyecto en particular corre en un servidor Hetzner que también
aloja otro proyecto (Kuma Coffee), compartiendo un único Caddy entre ambos —
esa parte está marcada explícitamente más abajo porque difiere de un
despliegue "solo".

## 0. Requisitos antes de empezar

- Una VPS con Ubuntu 22.04 o 24.04, con Docker y Docker Compose instalados.
- Acceso SSH a la VPS.
- Un dominio (o subdominio gratis de [DuckDNS](https://www.duckdns.org/))
  apuntando con un registro **A** a la IP pública de la VPS, para que Caddy
  pueda emitir el certificado TLS automáticamente.
- Si el servidor ya aloja otro proyecto con Caddy corriendo en los puertos
  80/443, ver la sección 5 (**Caddy compartido**) en vez de traer un Caddy
  propio.

## 1. Instala Docker en la VPS (si no lo tienes ya)

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Cierra sesión y vuelve a entrar por SSH para que el cambio de grupo aplique.
Verifica:

```bash
docker --version
docker compose version
```

## 2. Abre el firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 3. Clona el proyecto

```bash
git clone https://github.com/buriticaaguirrejuancarlos776-alt/lectosoft.git
cd lectosoft
```

## 4. Configura el `.env`

```bash
cp .env.example .env
nano .env
```

Nota que `DB_HOST` debe ser `db` (el nombre del servicio de MySQL en
`docker-compose.yml`), no `localhost`:

```
DJANGO_SECRET_KEY=<genera una nueva, ver abajo>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tu-dominio.duckdns.org
DJANGO_CSRF_TRUSTED_ORIGINS=https://tu-dominio.duckdns.org

DB_NAME=lectosoft
DB_USER=lectosoft_user
DB_PASSWORD=<una clave fuerte>
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=<otra clave fuerte, distinta>

EMAIL_HOST_USER=<cuenta de Gmail>
EMAIL_HOST_PASSWORD=<contraseña de aplicación de Gmail>
```

Genera una `SECRET_KEY` nueva:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

## 5. Caddy: propio o compartido

### Opción A — Caddy propio (servidor dedicado solo a este proyecto)

Agrega un servicio `caddy` a `docker-compose.yml` con el `Caddyfile`:

```
tu-dominio.duckdns.org {
    encode gzip
    reverse_proxy web:8000
}
```

(El estático lo sirve WhiteNoise y el media Django directamente — ver
sección "Notas" — así que Caddy no necesita montar ningún volumen de la app.)

### Opción B — Caddy compartido con otros proyectos (este es el caso real)

Este `docker-compose.yml` **no trae su propio Caddy**: el servicio `web` se
conecta a una red externa (`caddy_net`) para que un Caddy independiente,
compartido con otros proyectos del mismo servidor, pueda alcanzarlo.

1. Crea la red compartida una sola vez (si no existe ya):
   ```bash
   docker network create caddy_net
   ```
2. Levanta un stack de Caddy independiente en su propia carpeta (ej.
   `~/caddy/`), fuera de este repo, con un servicio `caddy` conectado a
   `caddy_net` y un bloque por dominio en su `Caddyfile`:
   ```
   tu-dominio.duckdns.org {
       encode gzip
       reverse_proxy lectosoft_web:8000
   }
   ```
   `lectosoft_web` es el `container_name` fijo que ya trae el servicio `web`
   de este `docker-compose.yml`, alcanzable porque ambos comparten `caddy_net`.
3. Cada vez que agregues un dominio nuevo a ese Caddyfile:
   ```bash
   cd ~/caddy && docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
   ```

## 6. Levanta los contenedores

```bash
docker compose up -d --build
```

Esto construye la imagen de Django, levanta MySQL y corre las migraciones
automáticamente (parte del comando de arranque del servicio `web`).

Verifica que los servicios estén corriendo:

```bash
docker compose ps
```

### Si vienes de una base de datos existente (dump)

Antes de levantar `web`, con `db` ya arriba y healthy:

```bash
docker compose up -d db
DB_ROOT_PASSWORD=$(grep '^DB_ROOT_PASSWORD=' .env | cut -d= -f2-)
DB_NAME=$(grep '^DB_NAME=' .env | cut -d= -f2-)
docker compose exec -T db mysql -u root -p"$DB_ROOT_PASSWORD" "$DB_NAME" < tu_dump.sql
docker compose up -d --build
```

Antes de importar, comprueba que el dump coincide con el estado actual de
los modelos (que no haya migraciones pendientes sin aplicar):

```bash
python manage.py makemigrations --check --dry-run
```

### Media existente que no está en el dump

Las imágenes subidas (`media/`) no viajan en el dump ni, si el volumen es
nuevo, se copian solas desde la imagen. Cópialas a mano una vez:

```bash
# desde tu computador
scp -r media root@<ip-del-servidor>:~/lectosoft_media_seed

# en el servidor
cd ~/lectosoft
docker compose cp ~/lectosoft_media_seed/. web:/app/media/
rm -rf ~/lectosoft_media_seed
```

## 7. Crea el superusuario

Si el dump no traía ninguno (o es un despliegue nuevo):

```bash
docker compose exec web python manage.py createsuperuser
```

## 8. Prueba

Visita `https://tu-dominio.duckdns.org` y revisa:

- Que cargue el home con estilos (`/static/`, servido por WhiteNoise dentro
  del contenedor `web`).
- Que carguen las imágenes de cuentos/rompecabezas (`/media/`, servido por
  Django directamente, no por Caddy — ver "Notas" abajo).
- Panel de administración en `/admin/`.

## 9. Actualizaciones futuras (manuales)

```bash
cd ~/lectosoft
git pull
docker compose up -d --build
```

Las migraciones se aplican automáticamente al reiniciar el servicio `web`.

## 10. Comandos útiles

```bash
docker compose logs -f web         # logs de Django/gunicorn
docker compose logs -f db          # logs de MySQL
docker compose exec web python manage.py <comando>   # cualquier comando de manage.py
docker compose down                 # detener todo (los datos persisten en volúmenes)
```

## 11. Despliegue automático con GitHub Actions

Cada push a `main` se despliega solo, sin entrar por SSH manualmente. El
workflow está en `.github/workflows/deploy.yml` y usa `scripts/deploy.sh`,
que además:

- Hace un backup (`mysqldump`) de la base de datos **antes** de reconstruir
  los contenedores, guardado en `~/lectosoft_backups/` en el servidor
  (conserva los últimos 2).
- Nunca borra volúmenes: los datos de MySQL y el media viven en volúmenes
  con nombre (`mysql_data`, `media_data`) que persisten entre despliegues.
- Verifica, tras el `docker compose up -d --build`, que los contenedores
  `web` y `db` sigan corriendo. Si alguno murió, el workflow falla y muestra
  los últimos logs, en vez de dejar el sitio caído en silencio.

### Configuración inicial (una sola vez)

**1. Genera un par de llaves SSH dedicado para el despliegue** (recomendado:
no reutilizar tu llave personal de SSH):

```bash
ssh-keygen -t ed25519 -f ./deploy_key -N "" -C "github-actions-deploy"
```

**2. Autoriza la llave pública en el servidor:**

```bash
cat deploy_key.pub | ssh root@<ip-del-servidor> "cat >> ~/.ssh/authorized_keys"
```

**3. Crea estos secrets en GitHub** (`Settings > Secrets and variables >
Actions > New repository secret`):

| Secret | Valor |
|---|---|
| `DEPLOY_HOST` | IP o dominio del servidor |
| `DEPLOY_USER` | `root` |
| `DEPLOY_SSH_KEY` | Contenido completo de `deploy_key` (la llave **privada**) |

**4. Borra `deploy_key` y `deploy_key.pub` de tu computador** una vez
copiada la privada al secret.

A partir de aquí, cada push a `main` dispara el despliegue automáticamente;
puedes ver el progreso y los logs en la pestaña **Actions** del repositorio.

### Restaurar un backup si algo sale mal

```bash
ssh root@<ip-del-servidor>
cd ~/lectosoft
ls ~/lectosoft_backups/                # elige el backup a restaurar
docker compose exec -T db mysql -u root -p"$(grep DB_ROOT_PASSWORD .env | cut -d= -f2)" "$(grep DB_NAME .env | cut -d= -f2)" < ~/lectosoft_backups/backup_XXXXXXXX_XXXXXX.sql
```

## Notas de esta app en particular

- **Estático**: lo sirve WhiteNoise vía middleware, en cualquier entorno.
- **Media**: en producción (`DEBUG=False`) lo sirve Django directamente con
  la vista `django.views.static.serve` (montada explícitamente en
  `proyecto/urls.py`), no el helper `static()` de Django — ese helper hace
  no-op cuando `DEBUG=False` sin importar dónde se llame. Esto evita que
  Caddy necesite acceso al volumen de media, útil cuando Caddy es un stack
  independiente compartido con otros proyectos (Opción B de la sección 5).
- El almacenamiento de estáticos usa `whitenoise.storage.CompressedStaticFilesStorage`
  (sin hash/manifiesto) en vez de `CompressedManifestStaticFilesStorage`
  porque `aplicacion/static/inicio_sesion/css/inicio_sesion.css` referencia
  una fuente que no existe en el repo (`MeeraInimai.ttf`); con la variante de
  manifiesto, `collectstatic` falla al no poder resolver esa referencia.
