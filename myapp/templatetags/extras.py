from django import template

register = template.Library()

@register.filter
def remove_spaces_and_newlines(value):
    return value.replace(" ", "").replace("\n", "").replace("\r", "")
