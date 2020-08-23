import random

from Settings import POPULATION_SIZE, INFECTION_CHANCE, SECONDARY_INFECTION_CHANCE
from Person import Person

from Utilities import roll


class Population:

    def __init__(self):
        self.size = POPULATION_SIZE

        self.people = [Person(self, i) for i in range(self.size)]

        self.infection_stats = {
            'healthy': self.size,
            'healthy_percentage': 0,

            'infected_unknown': 0,
            'infected_known': 0,
            'infected_total': 0,
            'infected_percentage': 0,

            'recovered': 0,
            'recovered_percentage': 0,

            'dead': 0,
            'dead_percentage': 0,
        }

        self.index = 0


    def update_infection_stats(self):
        self.infection_stats['infected_total'] = self.infection_stats['infected_unknown'] + self.infection_stats['infected_known']

        self.infection_stats['infected_percentage'] = round((self.infection_stats['infected_total'] / self.size) * 100, 2)
        self.infection_stats['healthy_percentage'] = round((self.infection_stats['healthy'] / self.size) * 100, 2)
        self.infection_stats['recovered_percentage'] = round((self.infection_stats['recovered'] / self.size) * 100, 2)
        self.infection_stats['dead_percentage'] = round((self.infection_stats['dead'] / self.size) * 100, 2)


    def pass_day(self):
        for person in self.people:

            for _ in range(person.contacts_per_day):
                contact = self.people[random.randrange(0, self.size)]

                if person.status in [0, 3] and contact.status in [1, 2]:
                    if roll(INFECTION_CHANCE):
                        if person.status == 0:
                            person.infect()
                        elif person.status == 3:
                            if roll(SECONDARY_INFECTION_CHANCE):
                                person.infect()

                if person.status in [1, 2] and contact.status in [0, 3]:
                    if roll(INFECTION_CHANCE):
                        if contact.status == 0:
                            contact.infect()
                        elif contact.status == 3:
                            if roll(SECONDARY_INFECTION_CHANCE):
                                contact.infect()

            person.pass_day()


    def __iter__(self):
        self.index = 0
        return self


    def __next__(self):
        if self.index < len(self.people):
            selection = self.people[self.index]
            self.index += 1
            return selection
        else:
            raise StopIteration


    def __getitem__(self, item):
        return self.people[item]