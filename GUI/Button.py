import pygame

class Button:

    def __init__(self, text, x, y, width, height, border=False, colour=(0, 0, 0), text_colour=(255, 255, 255), border_colour=(255, 0, 0), border_width=1,
            callback=None, toggleable=False, alt_text=None):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))

        self.hovered = False
        self.selected = False
        self.toggleable = toggleable
        self.callback = callback

        self.text = text
        self.alt_text = alt_text if alt_text else self.text
        self.colour = colour
        self.hover_colour = (colour[0] + 20, colour[1] + 20, colour[1] + 20)
        self.text_colour = text_colour
        self.border = border
        self.border_colour = border_colour
        self.border_width = border_width

        self.text_font = pygame.font.SysFont('Arial', 20)
        self.text_render = self.text_font.render(self.text, 1, self.text_colour)
        self.alt_text_render = self.text_font.render(self.alt_text, 1, self.text_colour)



    def update(self, mpos):
        self.check_hovered(mpos)


    def draw(self, win):
        if self.hovered:
            self.surface.fill(self.hover_colour)
        else:
            self.surface.fill(self.colour)

        if not self.selected:
            self.surface.blit(
                self.text_render,
                ((self.width // 2 - self.text_render.get_width() // 2),
                 (self.height // 2 - self.text_render.get_height() // 2))
            )
        else:
            self.surface.blit(
                self.alt_text_render,
                ((self.width // 2 - self.alt_text_render.get_width() // 2),
                 (self.height // 2 - self.alt_text_render.get_height() // 2))
            )

        if self.border:
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


    def click(self):
        if self.toggleable:
            self.selected = not self.selected

        if self.callback is None:
            return

        self.callback()