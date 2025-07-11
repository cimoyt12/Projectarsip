from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Check if value ends with arg (string)."""
    return str(value).lower().endswith(str(arg).lower())