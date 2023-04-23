from django import template
from apps.blog.models import Categoria

register = template.Library()

@register.tag

def categoria():
    return Categoria.objects.first()