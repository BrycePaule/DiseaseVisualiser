import pygame

from Settings.VisualiserSettings import NODE_COUNT, NODE_SIZE, VISUALISER_WINDOW_SIZE, GRID_COLOUR
from Visualiser.ColourLookup import colour_lookup

class Node:
    """
    Status :
        0 - healthy
        1 - infected_unknown
        2 - infected_known
        3 - recovered
        4 - dead
    """

    def __init__(self):
        self.status = 0

        self.size = NODE_SIZE
        self.surface = pygame.Surface((self.size, self.size))
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.colour = colour_lookup(self.status)
        self.desired_colour = colour_lookup(self.status)


    def draw(self):
        if self.colour != self.desired_colour:
            self.shift_overall_colour()
        self.surface.fill(self.colour)
        pygame.draw.rect(self.surface, GRID_COLOUR, self.rect, 1)

        return self.surface


    def shift_overall_colour(self):
        new_r = self.shift_clamp_channel(self.colour[0], self.desired_colour[0])
        new_g = self.shift_clamp_channel(self.colour[1], self.desired_colour[1])
        new_b = self.shift_clamp_channel(self.colour[2], self.desired_colour[2])

        self.colour = (new_r, new_g, new_b)


    def shift_clamp_channel(self, channel1, channel2, max_step=2):
        if channel1 != channel2:
            if channel1 < channel2:
                channel1 += min(max_step, max(0, abs(channel2 - channel1)))
            else:
                channel1 -= min(max_step, max(0, abs(channel2 - channel1)))

        return channel1


    def convert_healthy(self):
        self.status = 0
        self.desired_colour = colour_lookup(self.status)

    def convert_infected(self):
        self.status = 1
        self.desired_colour = colour_lookup(self.status)

    def convert_recovered(self):
        self.status = 3
        self.desired_colour = colour_lookup(self.status)

    def convert_dead(self):
        self.status = 4
        self.desired_colour = colour_lookup(self.status)