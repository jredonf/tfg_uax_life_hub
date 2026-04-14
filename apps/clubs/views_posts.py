"""Vistas de publicaciones y comentarios del modulo de clubes."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ClubPostCommentForm, ClubPostForm
from .models import ClubPost, ClubPostComment, ClubPostLike
from .permissions import user_can_manage_club
from .view_helpers import get_published_club, is_ajax_request, user_is_active_member


# Gestion de noticias y comentarios.
@require_POST
@login_required
def create_post_view(request, slug):
    """Publica una nueva noticia o comunicacion interna del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para publicar noticias.")

    form = ClubPostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.club = club
        post.author = request.user
        post.save()
        messages.success(request, "Noticia publicada.")
    else:
        messages.error(request, "No se pudo publicar la noticia.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def delete_post_view(request, slug, post_id):
    """Elimina una publicacion del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar noticias.")

    get_object_or_404(ClubPost, id=post_id, club=club).delete()
    messages.success(request, "Noticia eliminada.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def update_post_view(request, slug, post_id):
    """Actualiza una publicacion existente del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para editar noticias.")

    post = get_object_or_404(ClubPost, id=post_id, club=club)
    form = ClubPostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Noticia actualizada.")
    else:
        messages.error(request, "No se pudo actualizar la noticia.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def comment_post_view(request, slug, post_id):
    """Anade un comentario a una publicacion del club."""

    club = get_published_club(slug)
    if not user_is_active_member(request.user, club) and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("Solo los miembros pueden comentar.")

    post = get_object_or_404(ClubPost, id=post_id, club=club)
    form = ClubPostCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        if is_ajax_request(request):
            return JsonResponse(
                {
                    "ok": True,
                    "comment_id": comment.id,
                    "author": request.user.display_name,
                    "body": comment.body,
                    "comments_total": post.comments.count(),
                    "delete_url": reverse(
                        "clubs:delete_comment",
                        kwargs={"slug": club.slug, "post_id": post.id, "comment_id": comment.id},
                    ),
                }
            )
    else:
        error_message = "El comentario no puede superar los 500 caracteres."
        if is_ajax_request(request):
            return JsonResponse({"ok": False, "error": error_message}, status=400)
        messages.error(request, error_message)
    return redirect(f"{reverse('clubs:detail', kwargs={'slug': club.slug})}#post-{post.id}")


@require_POST
@login_required
def delete_comment_view(request, slug, post_id, comment_id):
    """Elimina un comentario propio o uno gestionado por responsables del club."""

    club = get_published_club(slug)
    post = get_object_or_404(ClubPost, id=post_id, club=club)
    comment = get_object_or_404(ClubPostComment, id=comment_id, post=post)

    if comment.author_id != request.user.id and not user_can_manage_club(request.user, club):
        if is_ajax_request(request):
            return JsonResponse(
                {"ok": False, "error": "No tienes permisos para eliminar este comentario."},
                status=403,
            )
        return HttpResponseForbidden("No tienes permisos para eliminar este comentario.")

    comment.delete()
    comments_total = post.comments.count()
    if is_ajax_request(request):
        return JsonResponse({"ok": True, "comments_total": comments_total})

    messages.success(request, "Comentario eliminado.")
    return redirect(f"{reverse('clubs:detail', kwargs={'slug': club.slug})}#post-{post.id}")


@require_POST
@login_required
def like_post_view(request, slug, post_id):
    """Alterna el estado de me gusta de una publicacion del club."""

    club = get_published_club(slug)
    if not user_is_active_member(request.user, club) and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("Solo los miembros pueden marcar like.")

    post = get_object_or_404(ClubPost, id=post_id, club=club)
    like, created = ClubPostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    if is_ajax_request(request):
        return JsonResponse(
            {
                "ok": True,
                "liked": created,
                "likes_total": post.likes.count(),
            }
        )
    return redirect(f"{reverse('clubs:detail', kwargs={'slug': club.slug})}#post-{post.id}")
