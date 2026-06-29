from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def vnd(value):
    """Format a numeric value as Vietnamese đồng without decimal noise."""
    if value in (None, ''):
        return '—'

    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value

    return f'{amount:,.0f}'.replace(',', '.') + ' ₫'
