import cProfile

from DiseaseAlgorithm.DiseaseSpread import DiseaseSpread
from Visualiser.Visualiser import Visualiser

profiler = cProfile.Profile()

spread = DiseaseSpread()
vis = Visualiser()
vis.run()


# profiler.enable()
# spread.run()
# profiler.disable()
# profiler.print_stats()

# profiler.dump_stats('profiler.pstat')
# profiler.dump_stats('profiler.txt')