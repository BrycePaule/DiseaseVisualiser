import matplotlib.pyplot as plt

from Settings.ProjectionSettings import SAVE_LOCATION, SAVE_PREFIX

class Grapher:

    def __init__(self, data):
        self.data = data

        self.save_prefix = f'run{SAVE_PREFIX}_'


    def line_graph(self, day, *keys, xlabel=None, ylabel=None):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        for key in keys:
            plt.plot(list(range(day+1)), [self.data[d][key.key] for d in range(day+1)], key.colour)

        plt.draw()
        plt.savefig(f'{SAVE_LOCATION}{self.save_prefix}day_{day}.png')