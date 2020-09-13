import pygame
from string import ascii_letters

from GUI.UIElements.UIObject import UIObject


class TextBox(UIObject):

    def __init__(self, text, x, y, width, height, ui_group=None, border=False, colour=(0, 0, 0), text_colour=(255, 255, 255),
                    alt_text_colour=(200, 200, 200), border_colour=(255, 0, 0), border_width=1, callback=None, selectable=False, toggleable=False, num_only=False,
                    text_suffix=None):

        super().__init__(text, x, y, width, height, ui_group=ui_group, border=border, colour=colour, text_colour=text_colour,
                            border_colour=border_colour, border_width=border_width, selectable=selectable, toggleable=toggleable)

        # SETTINGS
        self.callback = callback
        self.num_only = num_only
        self.text_suffix = f' {text_suffix}' if text_suffix else ''

        self.user_text = ''

        self.text_render = self.text_font.render(f'{self.text}{self.text_suffix}', 1, self.text_colour)
        self.alt_text_colour = alt_text_colour
        self.alt_text_render = self.text_font.render(self.text, 1, self.alt_text_colour)


    def draw(self, win):
        if self.hovered:
            self.surface.fill(self.hover_colour)
        elif self.selected:
            self.surface.fill(self.selected_colour)
        else:
            self.surface.fill(self.colour)

        if not self.selected:
            self.surface.blit(
                self.text_render,
                ((self.width // 2 - self.text_render.get_width() // 2),
                 (self.height // 2 - self.text_render.get_height() // 2))
            )
        else:
            if not self.user_text:
                self.alt_text_render = self.text_font.render(self.text, 1, self.alt_text_colour)
                self.surface.blit(
                    self.alt_text_render,
                    ((self.width // 2 - self.alt_text_render.get_width() // 2),
                     (self.height // 2 - self.alt_text_render.get_height() // 2)))

            elif self.user_text:
                self.alt_text_render = self.text_font.render(self.user_text, 1, self.alt_text_colour)
                self.surface.blit(
                    self.alt_text_render,
                    ((self.width // 2 - self.alt_text_render.get_width() // 2),
                     (self.height // 2 - self.alt_text_render.get_height() // 2)))

        if self.border:
            if self.selected:
                pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(0, 0, self.width, self.height), self.border_width)
            else:
                pygame.draw.rect(self.surface, self.border_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)

        win.blit(self.surface, (self.x, self.y))


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

        if self.selected and self.user_text:
            self.use()
        else:
            self.reset_selection()



    def click(self):
        if self.selectable:
            self.selected = not self.selected


    def use(self):
        if self.check_user_input():
            self.text = self.user_text
            self.text_render = self.text_font.render(f'{self.text}{self.text_suffix}', 1, self.text_colour)
            self.reset_selection()
        else:
            self.reset_selection()
            return

        if self.callback is None:
            return

        if float(self.text) % 1 == 0:
            self.callback(self, int(self.text))
        else:
            self.callback(self, float(self.text))


    def check_user_input(self):
        valid_chars = f'0123456789.{ascii_letters}'

        if self.num_only:
            valid_chars = valid_chars[:11]

        for s in self.user_text:
            if s not in valid_chars:
                return False

        return True


    def reset_selection(self):
        self.selected = False
        self.user_text = ''