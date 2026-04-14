from django.db import transaction

from .models import ClubMembership


@transaction.atomic
def request_membership(*, club, user):
    """Aprueba o reactiva la membresía del usuario en un club."""

    membership, _created = ClubMembership.objects.get_or_create(
        club=club,
        user=user,
        defaults={"status": ClubMembership.Status.APPROVED},
    )
    updated_fields = []

    # Garantiza que la membresía quede activa aunque ya existiera previamente.
    if membership.status != ClubMembership.Status.APPROVED:
        membership.status = ClubMembership.Status.APPROVED
        updated_fields.append("status")

    if membership.left_at is not None:
        membership.left_at = None
        updated_fields.append("left_at")

    if updated_fields:
        membership.save(update_fields=updated_fields)

    return membership
