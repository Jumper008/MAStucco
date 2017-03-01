from django import template

register = template.Library()

@register.filter()
def extend_work_phase(value):
    if value == 'AD':
        return 'Added'
    elif value == 'CU':
        return 'Cutting'
    elif value == 'MO':
        return 'Moulding'
    elif value == 'IN':
        return 'Installing'
    else:
        return 'Finished'