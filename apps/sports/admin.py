from django.contrib import admin

from .models import SportTeam


@admin.register(SportTeam)
class SportTeamAdmin(admin.ModelAdmin):
    """Administracion de equipos deportivos vinculados a clubes."""

    list_display = ("name", "club", "branch", "season", "active")
