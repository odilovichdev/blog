from django import template


register = template.Library()

@register.filter(name='capitalize_first')
def capitalize_first(value:str):
    if isinstance(value, str) and value:
        return value[0].upper() + value[1:]
    return value

