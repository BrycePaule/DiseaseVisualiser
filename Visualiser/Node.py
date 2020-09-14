import pygame

from Settings.VisualiserSettings import NODE_SIZE, GRID_COLOUR, ANIMATE_NODES, NODE_BORDER
from Visualiser.ColourLookup import colour_lookup

from functools import total_ordering

@total_ordering
class Node:
    """
    Status :
        0 - healthy
        1 - infected_unknown
        2 - infected_known
        3 - recovered
        4 - dead
    """

    def __init__(self, status=0, border=NODE_BORDER, animate=ANIMATE_NODES):
        self.status = status

        self.size = NODE_SIZE
        self.surface = pygame.Surface((self.size, self.size))
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.border = border
        self.animate = animate
        self.colour = colour_lookup(self.status)
        self.desired_colour = colour_lookup(self.status)

        self.colour_shift_max_step = 10


    def draw(self, no_anim=False):
        if self.animate:
            if self.colour != self.desired_colour:
                self.shift_overall_colour()

        if no_anim:
            self.colour = colour_lookup(self.status)

        self.surface.fill(self.colour)
        if self.border:
            pygame.draw.rect(self.surface, GRID_COLOUR, self.rect, 1)

        return self.surface


    def shift_overall_colour(self):
        new_r = self.shift_clamp_channel(self.colour[0], self.desired_colour[0])
        new_g = self.shift_clamp_channel(self.colour[1], self.desired_colour[1])
        new_b = self.shift_clamp_channel(self.colour[2], self.desired_colour[2])

        self.colour = (new_r, new_g, new_b)


    def shift_clamp_channel(self, channel1, channel2):
        if channel1 != channel2:
            if channel1 < channel2:
                channel1 += min(self.colour_shift_max_step, max(0, abs(channel2 - channel1)))
            else:
                channel1 -= min(self.colour_shift_max_step, max(0, abs(channel2 - channel1)))

        return channel1


    def convert_healthy(self):
        self.status = 0
        if self.animate:
            self.desired_colour = colour_lookup(self.status)
        else:
            self.colour = colour_lookup(self.status)

    def convert_infected(self):
        self.status = 1
        if self.animate:
            self.desired_colour = colour_lookup(self.status)
        else:
            self.colour = colour_lookup(self.status)

    def convert_recovered(self):
        self.status = 3
        if self.animate:
            self.desired_colour = colour_lookup(self.status)
        else:
            self.colour = colour_lookup(self.status)

    def convert_dead(self):
        self.status = 4
        if self.animate:
            self.desired_colour = colour_lookup(self.status)
        else:
            self.colour = colour_lookup(self.status)

    def __repr__(self):
        return f'<N: {self.status}>'

    # equals
    def __eq__(self, other):
        return self.status == other.status

    # less than
    def __lt__(self, other):
        return self.status < other.status

    # less than or equal
    def __le__(self, other):
        return self.status <= other.status

    # greater than
    def __gt__(self, other):
        return self.status > other.status

    # greater than or equal
    def __ge__(self, other):
        return self.status >= other.status

    # # positive
    # def __pos__(self):
    #     return self
    #
    # # negative
    # def __neg__(self):
    #     return Node(status=4)