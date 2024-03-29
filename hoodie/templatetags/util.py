import re

from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = "^" + reverse(pattern_or_urlname) + "$"
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context["request"].path
    if re.search(pattern, path):
        return "active"
    return ""


@register.filter
def get_type(value):
    return type(value).__name__


@register.filter
def prettify(value, sep="_"):
    return value.replace(sep, " ").capitalize()
