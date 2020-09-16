from SpreadProjection.Population import Population
from Grapher.Grapher import Grapher
from Grapher.GraphKey import GraphKey
from Utils.Utilities import days_to_readable_date_format, str_fill
from Settings.ProjectionSettingsPackage import ProjectionSettingsPackage

class VirusSpreadProjection:

    def __init__(self, virus, settings=ProjectionSettingsPackage()):
        self.virus = virus
        self.settings = settings
        self.population = Population(self.virus, self.settings.pop_size)
        self.daily_stats = {}

        self.grapher = Grapher(self.daily_stats)

        self.finished = False


    def infect_initial(self):
        for i in range(self.settings.starting_infections):
            self.population.people[i].infect()


    def pass_day(self, day, print_stats=False):
        self.population.pass_day()
        self.population.update_infection_stats()

        self.daily_stats[day] = self.population.virus_stats.copy()

        if print_stats:
            print(f'Day: {day} {days_to_readable_date_format(day)}')
            print(f'    - {str_fill("Healthy", 10)} {self.daily_stats[day]["healthy_percentage"]}% ({self.daily_stats[day]["healthy"]}/{self.population.size})')
            print(f'    - {str_fill("Infected", 10)} {self.daily_stats[day]["infected_percentage"]}% ({self.daily_stats[day]["infected_total"]}/{self.population.size})')
            print(f'    - {str_fill("Recovered", 10)} {self.daily_stats[day]["recovered_percentage"]}% ({self.daily_stats[day]["recovered"]}/{self.population.size})')
            print(f'    - {str_fill("Dead", 10)} {self.daily_stats[day]["dead_percentage"]}% ({self.daily_stats[day]["dead"]}/{self.population.size})')

        # if day % 50 == 0 or day == DAY_LIMIT:
        #     self.graph_result(day)

        return self.population.virus_stats


    def is_finished(self, day):
        if not self.daily_stats:
            return False

        if self.daily_stats[day]['infected_percentage'] >= 100:
            pass
            # return True

        if self.daily_stats[day]['infected_total'] == self.population.size:
            pass
            # return True

        if self.daily_stats[day]['dead'] == self.population.size:
            self.finished = True
            return True

        if self.daily_stats[day]['infected_total'] == 0:
            if self.daily_stats[day]['recovered'] > 0:
                self.finished = True
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