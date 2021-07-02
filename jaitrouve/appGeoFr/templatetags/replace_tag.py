from django import template

register = template.Library()

@register.filter
def replace_tag(value):
    return value[1:-1].replace("'", "")