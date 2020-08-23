import random

from Individual import Individual
from Population import Population
from Settings import BREEDER_COUNT, DIE_COUNT, FITNESS_LIMIT, GENE_LENGTH, GENERATION_LIMIT


class GeneticAlgorithm:

    def __init__(self):
        self.generation_limit = GENERATION_LIMIT
        self.fitness_limit = FITNESS_LIMIT

        self.population = Population()
        self.generation_count = 0

        self.best = []
        self.offspring = []


    def run(self):
        self.population.calculate_fitness()

        for generation in range(self.generation_limit):

            if self.best:
                if self.best[0].fitness >= self.fitness_limit:
                    # print(f'# {generation} - Fittest: {self.best[0]}')
                    return self.generation_count, self.population[0]

            self.generation_count += 1

            self.pass_one_day()

            self.selection()
            self.crossover()
            self.mutate()
            self.replace_weakest()

            self.population.calculate_fitness()

            # print(f'# {generation} - Fittest: {self.best[0]}')

        return self.generation_count, self.best[0]


    def selection(self):
        self.best = self.population[:BREEDER_COUNT]


    def crossover(self):
        self.offspring = []

        for _ in range(DIE_COUNT):
            crossover_point = random.randrange(0, GENE_LENGTH)

            parent1 = self.best[random.randrange(0, len(self.best))]
            parent2 = self.best[random.randrange(0, len(self.best))]

            offspring = Individual(genes=parent1.genes[:crossover_point] + parent2.genes[crossover_point:])

            self.offspring.append(offspring)


    def mutate(self):
        for individual in self.offspring:
            roll = random.randint(0, 100)
            if roll < 5:
                mutation_point = random.randrange(0, GENE_LENGTH)
                individual.genes[mutation_point] = abs(individual.genes[mutation_point] - 1)


    def replace_weakest(self):
        self.population.individuals[-len(self.offspring):] = self.offspring


    def pass_one_day(self):

        for individual in self.population:
            individual