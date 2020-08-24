import random

from Names import get_random_name
from Utilities import roll, status_to_text
from Settings import DIAGNOSE_DAYS, CONTACTS_PER_DAY_KNOWN, CONTACTS_PER_DAY_UNKNOWN_CARRIER, FATALITY_RATE, RECOVERY_DAYS


class Person:
    """
    Status :
        0 - healthy
        1 - infected_unknown
        2 - infected_known
        3 - recovered
        4 - dead
    """

    def __init__(self, population, id):
        self.id = id
        self.population = population
        self.name = get_random_name()
        self.status = 0

        self.contacts_per_day = CONTACTS_PER_DAY_UNKNOWN_CARRIER
        self.diagnose_days_left = 0
        self.recovery_days_left = 0

    def pass_day(self):
        if self.status in [0, 3, 4]: return

        if self.status == 1:
            if self.diagnose_days_left <= 0: return

            self.diagnose_days_left -= 1
            if self.diagnose_days_left == 0:
                self.infect_unknown_to_known()

        if self.status == 2:
            if self.recovery_days_left > 0:
                self.recovery_days_left -= 1
            else:
                if self.death_check():
                    self.die()
                else:
                    self.recover()

    def infect(self):
        if self.status == 0:
            self.population.stats['healthy'] -= 1
        elif self.status == 3:
            self.population.stats['recovered'] -= 1

        self.status = 1
        self.population.stats['infected_unknown'] += 1
        self.diagnose_days_left = DIAGNOSE_DAYS

    def infect_unknown_to_known(self):
        self.status = 2
        self.population.stats['infected_unknown'] -= 1
        self.population.stats['infected_known'] += 1
        self.contacts_per_day = CONTACTS_PER_DAY_KNOWN
        self.recovery_days_left = RECOVERY_DAYS

    def recover(self):
        self.status = 3
        self.population.stats['infected_known'] -= 1
        self.population.stats['recovered'] += 1

    def death_check(self):
        return roll(FATALITY_RATE)

    def die(self):
        self.status = 4
        self.population.stats['infected_known'] -= 1
        self.population.stats['dead'] += 1

    def __repr__(self):
        return f'<{self.name}, {self.id} , {status_to_text(self.status)}>'