import pygame

from Settings.VisualiserSettings import BG_COLOUR


class UIObject:

    def __init__(self, text, x, y, width, height, tag=None, ui_group=None, border=False,
                    colour=BG_COLOUR, hover_colour=(50, 50, 50), selected_colour=(100, 100, 100),
                    font='Arial', font_size=20, text_colour=(255, 255, 255),
                    border_colour=(0, 0, 0), border_selected_colour=(0, 255, 0), border_width=1,
                    selectable=False, toggleable=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))
        self.ui_group = ui_group
        self.tag = tag

        self.selectable = selectable
        self.toggleable = toggleable

        self.hovered = False
        self.selected = False
        self.toggle = False

        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.selected_colour = selected_colour
        self.text_colour = text_colour
        self.border = border
        self.border_colour = border_colour
        self.border_selected_colour = border_selected_colour
        self.border_width = border_width

        self.text_font = pygame.font.SysFont(font, font_size)
        self.text_render = self.text_font.render(self.text, 1, self.text_colour)


    def update(self, mpos):
        self.check_hovered(mpos)


    def draw(self, win):
        if self.hovered:
            self.surface.fill(self.hover_colour)
        elif self.selected:
            self.surface.fill(self.selected_colour)
        else:
            self.surface.fill(self.colour)

        self.surface.blit(
            self.text_render,
            ((self.width // 2 - self.text_render.get_width() // 2),
             (self.height // 2 - self.text_render.get_height() // 2))
        )

        if self.border:
            if self.selected:
                pygame.draw.rect(self.surface, self.border_selected_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)
            else:
                pygame.draw.rect(self.surface, self.border_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)

        win.blit(self.surface, (self.x, self.y))


    def check_hovered(self, mpos):
        x, y = mpos
        if self.rect.collidepoint(x, y):
            self.hovered = True
            return True
        else:
            self.hovered = False
            return False


    def check_selected(self, mpos):
        x, y = mpos
        if self.rect.collidepoint(x, y):
            self.selected = True
            return True
        else:
            self.selected = False
            return False


    def check_clicked(self, mpos):
        x, y = mpos
        if self.rect.collidepoint(x, y):
            return True

        self.selected = False


    def click(self):
        pass


    def use(self):
        pass


    def reset_selection(self):
        self.selected = False