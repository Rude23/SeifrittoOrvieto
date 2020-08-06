from datetime import time, date
from django.utils import timezone

#quick&dirty
OPEN_MORNING = time(hour=11, minute=30)
CLOSING_MORNING = time(hour=15,minute=0)

OPEN_AFTERNOON = time(17,30)
CLOSING_AFTERNOON = time(21,30)

def isOpen():

    if date.today().isoweekday() == 4:
        return False

    else:
        now = timezone.localtime(timezone.now()).time()

        return OPEN_MORNING <= now <= CLOSING_MORNING or OPEN_AFTERNOON <= now <= CLOSING_AFTERNOON
