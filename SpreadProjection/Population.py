import random
import numpy as np

from SpreadProjection.Person import Person

from Utils.Utilities import roll


class Population:

    def __init__(self, virus, size, ):
        self.index = 0
        self.virus = virus
        self.size = size
        self.people = np.array([Person(self, self.virus) for _ in range(self.size)])
        self.virus_stats = {
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


    def update_infection_stats(self):
        self.virus_stats['infected_total'] = self.virus_stats['infected_unknown'] + self.virus_stats['infected_known']

        self.virus_stats['infected_percentage'] = round((self.virus_stats['infected_total'] / self.size) * 100, 2)
        self.virus_stats['healthy_percentage'] = round((self.virus_stats['healthy'] / self.size) * 100, 2)
        self.virus_stats['recovered_percentage'] = round((self.virus_stats['recovered'] / self.size) * 100, 2)
        self.virus_stats['dead_percentage'] = round((self.virus_stats['dead'] / self.size) * 100, 2)


    def pass_day(self):
        for person in self.people:
            for _ in range(person.contacts_per_day):
                contact = self.people[int(self.size * random.random())]

                if person.status in [0, 3] and contact.status in [1, 2]:
                    if person.status == 0:
                        if roll(self.virus.infection_chance):
                            person.infect()
                    elif person.status == 3:
                        if roll(self.virus.reinfection_chance):
                            person.infect()

                if person.status in [1, 2] and contact.status in [0, 3]:
                    if contact.status == 0:
                        if roll(self.virus.infection_chance):
                            contact.infect()
                    elif contact.status == 3:
                        if roll(self.virus.reinfection_chance):
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