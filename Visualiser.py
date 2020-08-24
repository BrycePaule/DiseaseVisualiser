from Population import Population
from Grapher import Grapher
from GraphKey import GraphKey
from Settings.Settings import DAY_LIMIT
from Utilities import days_to_readable_date_format, str_fill


class Visualiser:

    def __init__(self):
        self.day_limit = DAY_LIMIT
        self.population = Population()
        self.daily_stats = {}

        self.grapher = Grapher(self.daily_stats)


    def run(self):
        for day in range(self.day_limit):
            self.population.pass_day()
            self.population.update_infection_stats()

            self.daily_stats[day] = self.population.stats.copy()

            print(f'Day: {day} {days_to_readable_date_format(day)}')
            print(f'    - {str_fill("Healthy", 10)} {self.daily_stats[day]["healthy_percentage"]}% ({self.daily_stats[day]["healthy"]}/{self.population.size})')
            print(f'    - {str_fill("Infected", 10)} {self.daily_stats[day]["infected_percentage"]}% ({self.daily_stats[day]["infected_total"]}/{self.population.size})')
            print(f'    - {str_fill("Recovered", 10)} {self.daily_stats[day]["recovered_percentage"]}% ({self.daily_stats[day]["recovered"]}/{self.population.size})')
            print(f'    - {str_fill("Dead", 10)} {self.daily_stats[day]["dead_percentage"]}% ({self.daily_stats[day]["dead"]}/{self.population.size})')

            # with open('testing.txt', mode='w') as f:
            #     for num in range(day):
            #         f.write(f'{self.daily_stats[num]}\n')

            if day % 50 == 0:
                self.grapher.line_graph(
                    day,
                    GraphKey('healthy', 'g'),
                    GraphKey('infected_total', '--r'),
                    GraphKey('recovered', 'y'),
                    GraphKey('dead', '--k')
                )

            if self.is_finished(day):
                self.grapher.line_graph(
                    day,
                    GraphKey('healthy', 'g'),
                    GraphKey('infected_total', '--r'),
                    GraphKey('recovered', 'y'),
                    GraphKey('dead', '--k')
                )
                return
        return


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