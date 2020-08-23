from Settings import POPULATION_SIZE
from Individual import Individual

class Population:

    def __init__(self):
        self.size = POPULATION_SIZE
        
        self.individuals = [Individual() for _ in range(self.size)]

        # iterable
        self.index = 0


    def calculate_fitness(self):
        for individual in self.individuals:
            individual.calculate_fitness()

        self.sort_by_fitness()


    def sort_by_fitness(self):
        self.individuals = sorted(self.individuals, key=lambda individual: individual.fitness, reverse=True)


    def __iter__(self):
        self.index = 0
        return self


    def __next__(self):
        if self.index < len(self.individuals):
            selection = self.individuals[self.index]
            self.index += 1
            return selection
        else:
            raise StopIteration


    def __getitem__(self, item):
        return self.individuals[item]