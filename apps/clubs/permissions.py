def user_can_manage_club(user, club):
    """Determina si un usuario puede gestionar operativamente un club."""

    if not user.is_authenticated:
        return False

    # Los administradores globales pueden gestionar cualquier club.
    if user.is_superuser or getattr(user, "role", "") == "admin":
        return True

    # Los responsables y administradores del propio club mantienen permisos de gestión.
    return club.memberships.filter(
        user=user,
        role_in_club__in=("manager", "admin"),
        status="approved",
        left_at__isnull=True,
    ).exists()
