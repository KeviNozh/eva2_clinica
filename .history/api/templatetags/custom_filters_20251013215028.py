from django import template
from datetime import date

register = template.Library()

@register.filter
def edad(fecha_nacimiento):
    if not fecha_nacimiento:
        return "N/A"
    today = date.today()
    return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))