import pygame

from GUI.UIElements.UIObject import UIObject


class Button(UIObject):

    def __init__(self, text, x, y, width, height, ui_group=None, border=False, colour=(0, 0, 0), text_colour=(255, 255, 255), border_colour=(255, 0, 0), border_width=1,
                    callback=None, selectable=False, toggleable=False, alt_text=None):

        super().__init__(text, x, y, width, height, ui_group=ui_group, border=border, colour=colour, text_colour=text_colour, border_colour=border_colour,
                            border_width=border_width, selectable=selectable, toggleable=toggleable)
        self.callback = callback

        self.alt_text = alt_text if alt_text else self.text
        self.alt_text_render = self.text_font.render(self.alt_text, 1, self.text_colour)


    def draw(self, win):
        if self.hovered:
            self.surface.fill(self.hover_colour)
        elif self.selected:
            self.surface.fill(self.selected_colour)
        else:
            self.surface.fill(self.colour)

        if not self.toggle:
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


    def click(self):
        if self.toggleable:
            self.toggle = not self.toggle

        self.use()


    def use(self):
        if self.callback is None:
            return

        self.callback(self)