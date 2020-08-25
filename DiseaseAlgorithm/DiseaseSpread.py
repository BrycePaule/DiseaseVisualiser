from DiseaseAlgorithm.Population import Population
from DiseaseAlgorithm.Grapher import Grapher
from DiseaseAlgorithm.GraphKey import GraphKey
from Settings.AlgorithmSettings import DAY_LIMIT
from Utilities import days_to_readable_date_format, str_fill

class DiseaseSpread:

    def __init__(self):
        self.population = Population()
        self.daily_stats = {}

        self.grapher = Grapher(self.daily_stats)


    def pass_day(self, day):
        self.population.pass_day()
        self.population.update_infection_stats()

        self.daily_stats[day] = self.population.stats.copy()

        print(f'Day: {day} {days_to_readable_date_format(day)}')
        print(f'    - {str_fill("Healthy", 10)} {self.daily_stats[day]["healthy_percentage"]}% ({self.daily_stats[day]["healthy"]}/{self.population.size})')
        print(f'    - {str_fill("Infected", 10)} {self.daily_stats[day]["infected_percentage"]}% ({self.daily_stats[day]["infected_total"]}/{self.population.size})')
        print(f'    - {str_fill("Recovered", 10)} {self.daily_stats[day]["recovered_percentage"]}% ({self.daily_stats[day]["recovered"]}/{self.population.size})')
        print(f'    - {str_fill("Dead", 10)} {self.daily_stats[day]["dead_percentage"]}% ({self.daily_stats[day]["dead"]}/{self.population.size})')

        # if day % 50 == 0 or day == DAY_LIMIT:
        #     self.graph_result(day)

        return self.population.stats


    def is_finished(self, day):
        if not self.daily_stats: return False

        if self.daily_stats[day]['infected_percentage'] >= 100:
            pass
            # return True

        if self.daily_stats[day]['infected_total'] == self.population.size:
            pass
            # return True

        if self.daily_stats[day]['dead'] == self.population.size:
            return True

        if self.daily_stats[day]['infected_total'] == 0:
            if self.daily_stats[day]['recovered'] > 0:
                return True

        return False


    def graph_result(self, day):
        self.grapher.line_graph(
            day,
            GraphKey('healthy', 'g'),
            GraphKey('infected_total', '--r'),
            GraphKey('recovered', 'y'),
            GraphKey('dead', '--k')
        )