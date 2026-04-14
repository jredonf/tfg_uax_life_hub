from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Representa al usuario autenticado de la plataforma universitaria."""

    class Role(models.TextChoices):
        STUDENT = "student", "Estudiante"
        MANAGER = "manager", "Responsable"
        ADMIN = "admin", "Administrador"

    # Rol funcional del usuario dentro de la plataforma.
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    # Informacion academica basica para personalizar la experiencia.
    degree = models.CharField(max_length=150, blank=True)
    campus = models.CharField(max_length=100, blank=True)
    # Imagen de perfil opcional mostrada en vistas y paneles internos.
    profile_image = models.ImageField(upload_to="accounts/profiles/", blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        # Prioriza el nombre completo cuando existe para mejorar la presentacion.
        return self.get_full_name() or self.username

    @property
    def avatar_initial(self):
        # Genera una inicial de respaldo para perfiles sin imagen.
        return self.display_name[:1].upper() if self.display_name else "U"
