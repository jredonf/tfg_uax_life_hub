def user_can_manage_sport(user, sport):
    """Comprueba si el usuario puede gestionar una liga de este deporte."""

    if not user.is_authenticated:
        return False

    if user.is_superuser or getattr(user, "role", "") == "admin":
        return True

    return sport.managers.filter(user=user).exists()
