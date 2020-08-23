import random

from Settings import GENE_LENGTH
from Person import Person

class Individual:
    """
    1 - healthy
    0 - infected

    fitness = +1 for every 1

    """

    def __init__(self, genes=None):
        self.gene_length = GENE_LENGTH

        if not genes:
            self.genes = [random.randint(0, 1) for _ in range(self.gene_length)]
        else:
            self.genes = genes

        self.fitness = 0


    def calculate_fitness(self):
        """
        In this example, fitness is basically how resistent a population is
        to COVID-19 infection.

        More 0s = more infections
        """

        self.fitness = sum([int(gene) for gene in self.genes])


    def __repr__(self):
        return f'<Individual:  {self.fitness}, {self.genes}>'