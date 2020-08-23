import cProfile

from Visualiser import Visualiser

profiler = cProfile.Profile()

vis = Visualiser()

for i in range(1):
    vis.population.people[i].infect()

profiler.enable()
vis.run()
profiler.disable()
profiler.print_stats()
# profiler.dump_stats('profiler.pstat')
profiler.dump_stats('profiler.txt')