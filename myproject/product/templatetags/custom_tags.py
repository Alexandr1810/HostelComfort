from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def attr(obj, attribute_name):
    return getattr(obj, attribute_name, '')

@register.filter
def call_method(obj, method_name):
    method = getattr(obj, method_name, None)
    if callable(method):
        return method()
    return ''
