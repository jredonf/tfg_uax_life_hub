from django.conf import settings
from django.db import models

from apps.clubs.models import Club


class ClubEvent(models.Model):
    """Define un evento organizado por un club dentro de la plataforma."""

    # Relacion con el club responsable de la actividad.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    # Ventana temporal del evento utilizada para agenda y control de acceso.
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    # Datos de ubicación física o virtual del evento.
    location = models.CharField(max_length=150, blank=True)
    location_url = models.URLField(blank=True, max_length=1000)
    # Límite máximo de asistentes previsto para la actividad.
    capacity = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ("start_datetime",)

    def __str__(self):
        return self.title


class ClubEventAttendance(models.Model):
    """Registra la asistencia confirmada de un usuario a un evento."""

    # Enlace al evento al que se inscribe el usuario.
    event = models.ForeignKey(ClubEvent, on_delete=models.CASCADE, related_name="attendances")
    # Usuario que confirma su participación en el evento.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="club_event_attendances",
    )
    # Número de acompañantes asociados a la misma reserva.
    companions_count = models.PositiveSmallIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
        ordering = ("joined_at",)

    def __str__(self):
        return f"{self.user} - {self.event}"


class ContactRequest(models.Model):
    """Guarda las consultas enviadas desde la página pública de contacto."""

    class QueryType(models.TextChoices):
        """Agrupa las áreas principales de consulta disponibles en el formulario."""

        CLUBS_ASSOCIATIONS = "clubs_associations", "Clubes / Asociaciones"
        FITNESS_CENTER = "fitness_center", "UAX Fitness Center"
        INTERNAL_LEAGUES = "internal_leagues", "Ligas internas"
        COMPETITION_TEAMS = "competition_teams", "Equipos de competición"
        INDIVIDUAL_SPORTS = "individual_sports", "Deportes individuales"
        TECHNICAL_SERVICE = "technical_service", "Servicio Técnico Web"

    # Identifica a la persona que envía la consulta.
    name = models.CharField(max_length=120)
    email = models.EmailField()
    # Clasifica el motivo principal del contacto.
    query_type = models.CharField(max_length=40, choices=QueryType.choices)
    # Guarda el tema concreto seleccionado dentro del área consultada.
    query_topic = models.CharField(max_length=170)
    # Guarda el detalle completo del mensaje recibido.
    message = models.TextField(max_length=1500)
    accepted_privacy = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-submitted_at",)
        verbose_name = "solicitud de contacto"
        verbose_name_plural = "solicitudes de contacto"

    def __str__(self):
        return f"{self.query_topic} - {self.name}"
