from django.contrib import admin

from .models import League, LeagueMatch, LeagueTeam, Sport, SportFacility, SportManager, SportTeam


class SportManagerInline(admin.TabularInline):
    model = SportManager
    extra = 1


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    """Administracion de deportes de ligas internas."""

    list_display = ("name", "active", "display_order")
    list_filter = ("active",)
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "image", "description", "active", "display_order")
    inlines = (SportManagerInline,)


@admin.register(SportFacility)
class SportFacilityAdmin(admin.ModelAdmin):
    """Administracion de instalaciones deportivas publicas."""

    list_display = ("name", "campus", "active", "display_order")
    list_filter = ("active",)
    search_fields = ("name", "campus", "summary", "sports")
    prepopulated_fields = {"slug": ("name",)}
    fields = (
        "name",
        "slug",
        "image",
        "campus",
        "summary",
        "sports",
        "schedule",
        "access",
        "map_url",
        "active",
        "display_order",
    )


class LeagueTeamInline(admin.TabularInline):
    model = LeagueTeam
    extra = 1


class LeagueMatchInline(admin.TabularInline):
    model = LeagueMatch
    extra = 1
    fields = ("match_day", "home_team", "away_team", "played_at", "location", "home_score", "away_score")


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    """Administracion de ligas internas."""

    list_display = ("name", "sport", "season", "active")
    list_filter = ("sport", "active", "season")
    search_fields = ("name", "sport__name")
    inlines = (LeagueTeamInline, LeagueMatchInline)


@admin.register(LeagueTeam)
class LeagueTeamAdmin(admin.ModelAdmin):
    """Administracion de equipos dentro de una liga."""

    list_display = ("name", "league", "captain_name", "active")
    list_filter = ("league__sport", "league", "active")
    search_fields = ("name", "captain_name")


@admin.register(LeagueMatch)
class LeagueMatchAdmin(admin.ModelAdmin):
    """Administracion de calendario y resultados."""

    list_display = ("league", "match_day", "home_team", "away_team", "home_score", "away_score", "played_at")
    list_filter = ("league__sport", "league")
    search_fields = ("home_team__name", "away_team__name")


@admin.register(SportTeam)
class SportTeamAdmin(admin.ModelAdmin):
    """Administracion de equipos deportivos vinculados a clubes."""

    list_display = ("name", "club", "sport", "branch", "season", "active")
    list_filter = ("sport", "branch", "active")
