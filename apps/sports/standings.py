def build_league_standings(league):
    """Calcula la clasificacion de una liga a partir de sus resultados."""

    table = {}
    for team in league.teams.all():
        table[team.id] = {
            "team": team,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0,
        }

    matches = league.matches.select_related("home_team", "away_team")
    for match in matches:
        if not match.has_result:
            continue

        home = table.get(match.home_team_id)
        away = table.get(match.away_team_id)
        if not home or not away:
            continue

        home["played"] += 1
        away["played"] += 1
        home["goals_for"] += match.home_score
        home["goals_against"] += match.away_score
        away["goals_for"] += match.away_score
        away["goals_against"] += match.home_score

        if match.home_score > match.away_score:
            home["wins"] += 1
            away["losses"] += 1
            home["points"] += 3
        elif match.home_score < match.away_score:
            away["wins"] += 1
            home["losses"] += 1
            away["points"] += 3
        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    standings = list(table.values())
    for row in standings:
        row["goal_difference"] = row["goals_for"] - row["goals_against"]

    standings.sort(
        key=lambda row: (
            row["points"],
            row["goal_difference"],
            row["goals_for"],
        ),
        reverse=True,
    )
    return standings
