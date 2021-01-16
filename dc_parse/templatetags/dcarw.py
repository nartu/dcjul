from django import template

register = template.Library()

@register.filter(name='get_at_index')
def get_at_index(list, index):
    if type(list) is dict:
        return list.get(index,None)
    else:
        if index >= len(list):
            return None
        return list[index]
