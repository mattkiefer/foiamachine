from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import make_aware

# started from the code of Casey Webster at
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/ddd39a02644540b7

# Define the weekday mnemonics to match the date.weekday function
(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)
weekends=(SAT,SUN)


def networkdays(start_date, end_date, holidays=[]):
    delta_days = (end_date - start_date).days + 1
    full_weeks, extra_days = divmod(delta_days, 7)
    # num_workdays = how many days/week you work * total # of weeks
    num_workdays = (full_weeks + 1) * (7 - len(weekends))
    # subtract out any working days that fall in the 'shortened week'
    for d in range(1, 8 - extra_days):
        if (end_date + timedelta(d)).weekday() not in weekends:
             num_workdays -= 1
    # skip holidays that fall on weekends
    holidays =  [timezone.make_aware(x, timezone.get_default_timezone()) for x in holidays if x.weekday() not in weekends]
    # subtract out any holidays 
    for d in holidays:
        if start_date <= d <= end_date:
            num_workdays -= 1
    return num_workdays

def _in_between(a,b,x):
    return a <= x <= b or b <= x <= a

def cmp(a, b):
    return (a > b) - (a < b)

def workday(start_date, days=0, holidays=[]):
    full_weeks, extra_days = divmod(days,7 - len(weekends))
    new_date = start_date + timedelta(weeks=full_weeks)
    for i in range(extra_days):
        new_date += timedelta(days=1)
        while new_date.weekday() in weekends:
            new_date += timedelta(days=1)
    # to account for days=0 case
    while new_date.weekday() in weekends:
        new_date += timedelta(days=1)

    # avoid this if no holidays
    if holidays:
        delta = timedelta(days=1 * cmp(days,0))
        # skip holidays that fall on weekends
        holidays =  [x for x in holidays if x.weekday() not in weekends ]
        holidays =  [x for x in holidays if x != start_date ]
        for d in sorted(holidays, reverse = (days < 0)):
            # if d in between start and current push it out one working day
            if _in_between(start_date, new_date, d):
                new_date += delta
                while new_date.weekday() in weekends:
                    new_date += delta
    return new_date