import cProfile

from DiseaseAlgorithm.VirusSpreadProjection import VirusSpreadProjection
from Visualiser.Visualiser import Visualiser
from DiseaseAlgorithm.VirusManager import VirusManager

profiler = cProfile.Profile()

vis = Visualiser()

profiler.enable()
vis.run()



# spread.run()
# profiler.disable()
# profiler.print_stats()

# profiler.dump_stats('profiler.pstat')
# profiler.dump_stats('profiler.txt')