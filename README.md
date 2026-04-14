# UAX Life Hub

Proyecto "UAX Life Hub": Plataforma web para la gestión integral de la vida universitaria

## Requisitos

- Python 3.11
- PostgreSQL

## Instalación base

1. Crear y activar un entorno virtual.
2. Instalar dependencias:

```powershell
.\.venv\Scripts\pip install -r requirements\base.txt
```

3. Crear un archivo `.env` a partir de `.env.example`.
4. Configurar las credenciales de PostgreSQL en `.env`.
5. Aplicar migraciones:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

6. Iniciar el servidor:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

## Variables de entorno

El proyecto usa `python-decouple` y espera estas variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`


## Instalación de la base de datos con DBeaver

El proyecto incluye una copia manual de la base de datos en formato `.backup` o `.sql` para restaurar directamente con DBeaver.
Ruta: BBDD- Backup/bbdd_uaxlifehub_14042026

### Opción 1: restaurar un archivo `.backup`

1. Crear en PostgreSQL una base de datos vacía con el mismo nombre configurado en `DB_NAME`.
2. Abrir DBeaver y conectarse al servidor PostgreSQL.
3. Hacer clic derecho sobre la base de datos creada.
4. Ir a `Tools > Restore` ó `Herramientas > Restaurar Backup`.
5. Seleccionar el archivo `.backup`.
6. Ejecutar la restauración y esperar a que termine.

### Opción 2: restaurar un archivo `.sql`

1. Crear en PostgreSQL una base de datos vacía con el mismo nombre configurado en `DB_NAME`.
2. Abrir DBeaver y conectarse a esa base de datos.
3. Abrir el archivo `.sql` en el editor SQL de DBeaver.
4. Ejecutar el script completo sobre la base de datos vacía.

### Comprobación final

Después de restaurar la base de datos, ejecutar:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Si la copia restaurada está completa, `migrate` no debería aplicar cambios nuevos y el proyecto debería arrancar con los datos ya cargados.


