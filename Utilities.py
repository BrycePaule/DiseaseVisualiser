import random

def roll(chance):
    throw = random.randrange(0, 10000)
    if throw < chance * 100:
        return True
    else:
        return False

def str_fill(string, n):
    if len(string) < n:
        return string + (' ' * (n - len(string)))

def days_to_readable_date_format(days):

    years = 0
    months = 0
    weeks = 0

    while days >= 0:
        if days >= 365:
            years += 1
            days -= 365

        elif days >= 30:
            months += 1
            days -= 30

        elif days >= 7:
            weeks += 1
            days -= 7
        else:
            break

    result = '('

    if years:
        result += f'{years}y'
    if months:
        result += f'{months}m'
    if weeks:
        result += f'{weeks}w'

    if result == '(':
        return ''
    else:
        result += f'{days}d)'

    return result

def status_to_text(status):
    states = {
        0: 'Healthy',
        1: 'Infected_unknown',
        2: 'Infected_known',
        3: 'Recovered',
        4: 'Dead',
    }
    return states[status]