from Population import Population
from Settings import DAY_LIMIT
from Utilities import days_to_readable_date_format, str_fill


class Visualiser:

    def __init__(self):
        self.day_limit = DAY_LIMIT
        self.population = Population()


    def run(self):
        for day in range(self.day_limit):
            if self.is_finished():
                return

            self.population.pass_day()
            self.population.update_infection_stats()

            print(f'Day: {day} {days_to_readable_date_format(day)}')
            print(f'    - {str_fill("Healthy", 10)} {self.population.infection_stats["healthy_percentage"]}% ({self.population.infection_stats["healthy"]}/{self.population.size})')
            print(f'    - {str_fill("Infected", 10)} {self.population.infection_stats["infected_percentage"]}% ({self.population.infection_stats["infected_total"]}/{self.population.size})')
            print(f'    - {str_fill("Recovered", 10)} {self.population.infection_stats["recovered_percentage"]}% ({self.population.infection_stats["recovered"]}/{self.population.size})')
            print(f'    - {str_fill("Dead", 10)} {self.population.infection_stats["dead_percentage"]}% ({self.population.infection_stats["dead"]}/{self.population.size})')

        return


    def is_finished(self):
        if self.population.infection_stats['infected_percentage'] >= 100:
            pass
            # return True
        if self.population.infection_stats['infected_total'] == self.population.size:
            pass
            # return True
        if self.population.infection_stats['infected_total'] == 0:
            if self.population.infection_stats['recovered'] > 0:
                return True

        return False