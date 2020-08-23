import random

from Settings import POPULATION_SIZE, CONTACTS_PER_DAY, INFECTION_CHANCE
from Person import Person

from Utilities import roll


class Population:

    def __init__(self):
        self.size = POPULATION_SIZE
        
        self.people = [Person(i) for i in range(self.size)]
        self.total_infected = 0
        self.infection_percentage = 0

        # iterable
        self.index = 0


    def calculate_infection_rate(self):
        self.total_infected = len(list(filter(lambda x: x.status == 1, self.people)))
        self.infection_percentage = int((self.total_infected / self.size) * 100)


    def spread(self):
        for person in self.people:
            if person.status == 0: continue

            flip = False
            for _ in range(CONTACTS_PER_DAY):
                flip = not flip
                if flip:
                    try:
                        contact = self.people[random.randrange(0, person.id)]
                    except ValueError:
                        contact = self.people[random.randrange(person.id + 1, self.size)]
                else:
                    try:
                        contact = self.people[random.randrange(person.id + 1, self.size)]
                    except ValueError:
                        contact = self.people[random.randrange(0, person.id)]

                if contact.status == 0:
                    if roll(INFECTION_CHANCE):
                        contact.status = 1


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