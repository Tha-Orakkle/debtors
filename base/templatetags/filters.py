from django import template
from datetime import datetime


register = template.Library()


# @register.filter(name='dt_format')
# def dt_format(value):
#     if value:
#         return value.split("T")[0]
#     return value

@register.filter(name='_float')
def _float(value):
    return "{:,.2f}".format(float(value))