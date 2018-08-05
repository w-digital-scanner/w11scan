from django import template

register = template.Library()

@register.filter(name='mongo2id')
def mongo2id(obj,attribute):
    return obj[attribute]

