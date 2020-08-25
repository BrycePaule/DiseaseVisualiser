from Settings.Names import get_random_name
from Utilities import roll, status_to_text

from Settings.AlgorithmSettings import CONTACTS_PER_DAY_KNOWN, CONTACTS_PER_DAY_UNKNOWN_CARRIER


class Person:
    """
    Status :
        0 - healthy
        1 - infected_unknown
        2 - infected_known
        3 - recovered
        4 - dead
    """

    def __init__(self, population, virus):
        self.population = population
        self.virus = virus

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
            self.population.virus_stats['healthy'] -= 1
        elif self.status == 3:
            self.population.virus_stats['recovered'] -= 1

        self.status = 1
        self.population.virus_stats['infected_unknown'] += 1
        self.diagnose_days_left = self.virus.diagnose_days

    def infect_unknown_to_known(self):
        self.status = 2
        self.population.virus_stats['infected_unknown'] -= 1
        self.population.virus_stats['infected_known'] += 1
        self.contacts_per_day = CONTACTS_PER_DAY_KNOWN
        self.recovery_days_left = self.virus.recovery_days

    def recover(self):
        self.status = 3
        self.population.virus_stats['infected_known'] -= 1
        self.population.virus_stats['recovered'] += 1

    def death_check(self):
        return roll(self.virus.fatality_chance)

    def die(self):
        self.status = 4
        self.population.virus_stats['infected_known'] -= 1
        self.population.virus_stats['dead'] += 1

    def __repr__(self):
        return f'<{self.name}, {status_to_text(self.status)}>'