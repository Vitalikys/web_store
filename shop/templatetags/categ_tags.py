#https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/
# in file.html  need to import this file
from django import template

from shop.models import Writer

register = template.Library()

# @register.simple_tag()
# def get_writers():
#     return Writer.objects.all()

@register.inclusion_tag('shop/writers_inclusion_tags.html')
def show_writers():
    writers = Writer.objects.all()
    return {"writers": writers}
