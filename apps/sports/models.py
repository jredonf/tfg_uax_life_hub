from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.clubs.models import Club


class Sport(models.Model):
    """Deporte disponible para las ligas internas."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="sports/images/", blank=True, null=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"

    def save(self, *args, **kwargs):
        # Genera el slug si todavia no se ha indicado desde el admin.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SportFacility(models.Model):
    """Instalacion deportiva mostrada en la pagina publica."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    image = models.ImageField(upload_to="sports/facilities/", blank=True, null=True)
    campus = models.CharField(max_length=150)
    summary = models.TextField()
    sports = models.TextField(help_text="Introduce un uso o deporte por linea.")
    schedule = models.CharField(max_length=150)
    access = models.CharField(max_length=180)
    map_url = models.URLField("Enlace de ubicacion", blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "Instalacion deportiva"
        verbose_name_plural = "Instalaciones deportivas"

    def save(self, *args, **kwargs):
        # Genera el slug si todavia no se ha indicado desde el admin.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def sport_list(self):
        # Los usos se guardan sencillos: una linea por etiqueta.
        return [sport.strip() for sport in self.sports.splitlines() if sport.strip()]


class SportManager(models.Model):
    """Usuario responsable de gestionar un deporte concreto."""

    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="managers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_sports")

    class Meta:
        unique_together = ("sport", "user")
        ordering = ("sport__name", "user__username")
        verbose_name = "Responsable de deporte"
        verbose_name_plural = "Responsables de deporte"

    def __str__(self):
        return f"{self.user} - {self.sport}"


class SportTeam(models.Model):
    """Representa un equipo deportivo vinculado a un club universitario."""

    class Branch(models.TextChoices):
        MALE = "male", "Masculino"
        FEMALE = "female", "Femenino"
        MIXED = "mixed", "Mixto"
        INDIVIDUAL = "individual", "Individual"

    # Club al que pertenece el equipo deportivo.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="teams")
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT, related_name="club_teams", blank=True, null=True)
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


class League(models.Model):
    """Liga interna de un deporte y temporada concreta."""

    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="leagues")
    name = models.CharField(max_length=150)
    season = models.CharField(max_length=20, default="2025/2026")
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sport__display_order", "name")
        unique_together = ("sport", "name", "season")
        verbose_name = "Liga interna"
        verbose_name_plural = "Ligas internas"

    def __str__(self):
        return f"{self.name} - {self.season}"


class LeagueTeam(models.Model):
    """Equipo participante en una liga interna."""

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=150)
    captain_name = models.CharField(max_length=120, blank=True)
    players = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("league", "name")
        verbose_name = "Equipo de liga"
        verbose_name_plural = "Equipos de liga"

    def __str__(self):
        return self.name

    @property
    def player_list(self):
        # La plantilla se guarda sencilla: una linea por jugador.
        return [player.strip() for player in self.players.splitlines() if player.strip()]


class LeagueMatch(models.Model):
    """Partido del calendario de una liga interna."""

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="matches")
    match_day = models.PositiveIntegerField(default=1)
    home_team = models.ForeignKey(LeagueTeam, on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(LeagueTeam, on_delete=models.CASCADE, related_name="away_matches")
    played_at = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True)
    home_score = models.PositiveIntegerField(blank=True, null=True)
    away_score = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ("played_at", "match_day", "id")
        verbose_name = "Partido de liga"
        verbose_name_plural = "Partidos de liga"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

    def clean(self):
        # Evita crear partidos con equipos de otra liga.
        if self.home_team_id and self.home_team.league_id != self.league_id:
            raise ValidationError("El equipo local no pertenece a esta liga.")
        if self.away_team_id and self.away_team.league_id != self.league_id:
            raise ValidationError("El equipo visitante no pertenece a esta liga.")
        if self.home_team_id and self.home_team_id == self.away_team_id:
            raise ValidationError("Un equipo no puede jugar contra si mismo.")

    @property
    def has_result(self):
        return self.home_score is not None and self.away_score is not None
