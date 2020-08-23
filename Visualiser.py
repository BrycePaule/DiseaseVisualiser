import time

from Population import Population
from Settings import DAY_LIMIT


class Visualiser:

    def __init__(self):
        self.day_limit = DAY_LIMIT

        self.population = Population()
        self.day_count = 0


    def run(self):
        for day in range(self.day_limit):

            if self.population.infection_percentage == 100:
                return self.day_count

            self.day_count += 1

            self.pass_one_day()

            print(f'Day: {day}')
            print(f'    - Infected {self.population.infection_percentage}% ({self.population.total_infected}/{self.population.size})')

        return self.day_count



    def pass_one_day(self):
        self.population.spread()
        self.population.calculate_infection_rate()
        time.sleep(0.2)