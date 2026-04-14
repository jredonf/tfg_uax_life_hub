from django import template

from apps.clubs.rich_text import render_rich_text


register = template.Library()


@register.filter
def rich_text(value):
    return render_rich_text(value)
