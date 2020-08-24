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


    def draw(self):
        self.surface.fill(colour_lookup(self.status))
        pygame.draw.rect(self.surface, GRID_COLOUR, self.rect, 1)

        return self.surface