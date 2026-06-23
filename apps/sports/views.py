from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from .forms import LeagueMatchResultForm
from .models import LeagueMatch, Sport
from .permissions import user_can_manage_sport
from .standings import build_league_standings


class SportListView(TemplateView):
    """Muestra la pagina publica de ligas internas."""

    template_name = "sports/sport_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sports = Sport.objects.filter(active=True).prefetch_related(
            "managers",
            "leagues__teams",
            "leagues__matches__home_team",
            "leagues__matches__away_team",
        )

        sports_data = []
        for sport in sports:
            leagues_data = []
            can_manage = user_can_manage_sport(self.request.user, sport)

            for league in sport.leagues.filter(active=True):
                teams = league.teams.filter(active=True)
                leagues_data.append(
                    {
                        "league": league,
                        "teams": teams,
                        "matches": league.matches.select_related("home_team", "away_team"),
                        "standings": build_league_standings(league),
                    }
                )

            total_teams = sum(league_data["teams"].count() for league_data in leagues_data)
            total_matches = sum(league_data["matches"].count() for league_data in leagues_data)
            sports_data.append(
                {
                    "sport": sport,
                    "leagues": leagues_data,
                    "can_manage": can_manage,
                    "league_count": len(leagues_data),
                    "team_count": total_teams,
                    "match_count": total_matches,
                }
            )

        context["sports_data"] = sports_data
        return context


@login_required
def update_match_result_view(request, match_id):
    """Actualiza el resultado de un partido desde la pagina de ligas."""

    match = get_object_or_404(LeagueMatch.objects.select_related("league__sport"), pk=match_id)
    sport = match.league.sport

    if not user_can_manage_sport(request.user, sport):
        return HttpResponseForbidden("No tienes permisos para editar esta liga.")

    if request.method == "POST":
        form = LeagueMatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, "Resultado actualizado correctamente.")
        else:
            messages.error(request, "Revisa el resultado introducido.")

    return redirect("sports:list")
