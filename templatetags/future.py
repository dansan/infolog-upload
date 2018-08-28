from django.template import Library
from django.template.defaulttags import url as url_ori

register = Library()

@register.tag
def url(*args, **kwargs):
    return url_ori(*args, **kwargs)

