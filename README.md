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

