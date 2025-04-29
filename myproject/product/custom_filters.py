from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary and key in dictionary:
        return dictionary[key]
    return None

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.filter
def call_method(obj, method_name):
    method = getattr(obj, method_name, None)
    if callable(method):
        return method()
    return None
