from datetime import datetime, timedelta
from dateutil import parser
from django import template
from django.utils.timesince import timesince
from socialdistribution.settings import LOCAL_HOST

import pytz

register = template.Library()

# http://stackoverflow.com/questions/6494921/how-to-display-x-days-ago-type-time-using-humanize-in-django-template

@register.filter
def datesince(value):
    now = datetime.now(pytz.utc)
    try:
        date = parser.parse(value)
        difference = now - date
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(date).split(', ')[0]}

@register.filter
def islocal(value):
    return value == LOCAL_HOST