from django import forms

from .models import LeagueMatch


class LeagueMatchResultForm(forms.ModelForm):
    """Formulario simple para actualizar resultados de partidos."""

    class Meta:
        model = LeagueMatch
        fields = ("home_score", "away_score")
        labels = {
            "home_score": "Local",
            "away_score": "Visitante",
        }
        widgets = {
            "home_score": forms.NumberInput(attrs={"min": 0, "placeholder": "0"}),
            "away_score": forms.NumberInput(attrs={"min": 0, "placeholder": "0"}),
        }
