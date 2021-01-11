from urllib.parse import urlencode
from django import template

from ebapp.models import Auctions

register = template.Library()

@register.simple_tag(takes_context=True)
def url_auctions_replace(context, **kwargs):

    query = context['request'].GET.copy()

    page = kwargs.pop('page')

    url_page = f'page-{page}/'

    question_mark = '?' if bool(query) else ''

    return f'/auctions/{url_page}{question_mark}{urlencode(query)}'

@register.simple_tag(takes_context=True)
# def auction_notconfirmed_counter 
def counter(context, **kwargs):

    auctions_count = Auctions.objects.filter(status__exact = 0, archived__exact=0).count()

    return auctions_count