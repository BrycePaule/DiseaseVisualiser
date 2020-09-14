import pygame

from Visualiser.UI.UIElements.UIObject import UIObject


class Button(UIObject):

    def __init__(self, text, x, y, width, height, tag=None, ui_group=None, border=False,
                    colour=(60, 60, 60), hover_colour=(80, 80, 80), selected_colour=(100, 100, 100),
                    font='Arial', font_size=20, text_colour=(255, 255, 255),
                    border_colour=(30, 30, 30), border_selected_colour=(150, 150, 150), border_width=1,
                    selectable=False, toggleable=False, callback=None, callback_rv=None, alt_text=None):

        super().__init__(text, x, y, width, height, tag=tag, ui_group=ui_group, border=border,
                         colour=colour, hover_colour=hover_colour, selected_colour=selected_colour,
                         font=font, font_size=font_size, text_colour=text_colour,
                         border_colour=border_colour, border_selected_colour=border_selected_colour, border_width=border_width,
                         selectable=selectable, toggleable=toggleable)

        self.callback = callback
        self.callback_rv = callback_rv

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
            if self.selected:
                pygame.draw.rect(self.surface, self.border_selected_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)
            else:
                pygame.draw.rect(self.surface, self.border_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)

        win.blit(self.surface, (self.x, self.y))


    def click(self):
        if self.toggleable:
            self.toggle = not self.toggle

        if self.selectable:
            self.selected = not self.selected

        self.use()


    def use(self):
        if self.callback is None:
            return

        if self.callback_rv:
            try:
                rv = getattr(self, self.callback_rv)
                self.callback(rv)
            except ValueError:
                pass
        else:
            self.callback()