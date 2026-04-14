from django.db import models

from apps.clubs.models import Club


class SportTeam(models.Model):
    """Representa un equipo deportivo vinculado a un club universitario."""

    class Branch(models.TextChoices):
        MALE = "male", "Masculino"
        FEMALE = "female", "Femenino"
        MIXED = "mixed", "Mixto"
        INDIVIDUAL = "individual", "Individual"

    # Club al que pertenece el equipo deportivo.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=150)
    # Modalidad o rama competitiva del equipo.
    branch = models.CharField(max_length=20, choices=Branch.choices)
    coach_name = models.CharField(max_length=120, blank=True)
    season = models.CharField(max_length=20, blank=True)
    # Permite ocultar equipos historicos sin eliminarlos.
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
