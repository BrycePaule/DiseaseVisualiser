import pygame

from GUI.UIElements.UIObject import UIObject

class Text(UIObject):

    def __init__(self, text, x, y, width, height, ui_group=None, border=False,
                    colour=(0, 0, 0), hover_colour=(50, 50, 50), selected_colour=(100, 100, 100),
                    font='Arial', font_size=20, text_colour=(255, 255, 255),
                    border_colour=(255, 0, 0), border_width=1,
                    selectable=False, toggleable=False, background=False, align='left'):

        super().__init__(text, x, y, width, height, ui_group=ui_group, border=border,
                         colour=colour, hover_colour=hover_colour, selected_colour=selected_colour,
                         font=font, font_size=font_size, text_colour=text_colour,
                         border_colour=border_colour, border_width=border_width,
                         selectable=selectable, toggleable=toggleable)

        self.selectable = False
        self.toggleable = False

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background = background
        self.align = align

    def draw(self, win):
        if self.background:
            self.surface.fill(self.colour)
        else:
            transparent_fill = (self.colour[0], self.colour[1], self.colour[2], 0)
            self.surface.fill(transparent_fill)

        if self.align == 'centre':
            self.surface.blit(
                self.text_render,
                ((self.width // 2 - self.text_render.get_width() // 2),
                 (self.height // 2 - self.text_render.get_height() // 2))
            )
        elif self.align == 'left':
            self.surface.blit(
                self.text_render,
                (0, self.height // 2 - self.text_render.get_height() // 2))

        if self.border:
            pygame.draw.rect(self.surface, self.border_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)

        win.blit(self.surface, (self.x, self.y))