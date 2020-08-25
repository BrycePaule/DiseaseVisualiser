import cProfile

from DiseaseAlgorithm.DiseaseSpread import DiseaseSpread
from Visualiser.Visualiser import Visualiser
from DiseaseAlgorithm.DiseaseManager import DiseaseManager

profiler = cProfile.Profile()

vis = Visualiser()

profiler.enable()
vis.run()



# spread.run()
# profiler.disable()
# profiler.print_stats()

# profiler.dump_stats('profiler.pstat')
# profiler.dump_stats('profiler.txt')