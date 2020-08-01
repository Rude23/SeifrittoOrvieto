from datetime import time
from django import template
from django.utils import timezone

#quick&dirty
OPEN_MORNING = time(hour=12, minute=0)
CLOSING_MORNING = time(hour=14,minute=0)

OPEN_AFTERNOON = time(17,0)
CLOSING_AFTERNOON = time(22,0)

register=template.Library()

@register.filter(name="isOpen")
def isOpen():
    now=timezone.localtime(timezone.now()).time()

    return OPEN_MORNING <= now <=CLOSING_MORNING or OPEN_AFTERNOON <= now <=CLOSING_AFTERNOON
