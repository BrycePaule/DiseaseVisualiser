import pygame
from string import ascii_letters

from Visualiser.UI.UIElements.UIObject import UIObject


class TextBox(UIObject):

    def __init__(self, text, x, y, width, height, tag=None, ui_group=None, border=False,
                    colour=(60, 60, 60), hover_colour=(80, 80, 80), selected_colour=(100, 100, 100),
                    font='Arial', font_size=20, text_colour=(150, 150, 150), alt_text_colour=(255, 255, 255),
                    border_colour=(30, 30, 30), border_selected_colour=(150, 150, 150), border_width=1,
                    selectable=False, toggleable=False, callback=None, num_only=False, int_only=False, text_suffix=None):

        super().__init__(text, x, y, width, height, tag=tag, ui_group=ui_group, border=border,
                         colour=colour, hover_colour=hover_colour, selected_colour=selected_colour,
                         font=font, font_size=font_size, text_colour=text_colour,
                         border_colour=border_colour, border_selected_colour=border_selected_colour, border_width=border_width,
                         selectable=selectable, toggleable=toggleable)

        # SETTINGS
        self.callback = callback
        self.num_only = num_only
        self.int_only = int_only
        self.text_suffix = f'{text_suffix}' if text_suffix else ''

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
            self.alt_text_render = self.text_font.render(f'{self.user_text}|', 1, self.alt_text_colour)
            self.surface.blit(
                self.alt_text_render,
                ((self.width // 2 - self.alt_text_render.get_width() // 2),
                 (self.height // 2 - self.alt_text_render.get_height() // 2)))

        if self.border:
            if self.selected:
                pygame.draw.rect(self.surface, self.border_selected_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)
            else:
                pygame.draw.rect(self.surface, self.border_colour, pygame.Rect(0, 0, self.width, self.height), self.border_width)

        win.blit(self.surface, (self.x, self.y))


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
        if self.user_text == self.text:
            self.reset_selection()
            return
        elif self.check_user_input():
            self.text = self.user_text
            self.text_render = self.text_font.render(f'{self.text}{self.text_suffix}', 1, self.text_colour)
            self.reset_selection()
        else:
            self.reset_selection()
            return

        if self.callback is None:
            return

        if float(self.text) % 1 == 0:
            self.callback(int(self.text))
        elif float(self.text) % 1 != 0:
            self.callback(float(self.text))
        else:
            self.callback(self.text)


    def check_user_input(self):
        if not self.user_text:
            return False

        valid_chars = f'0123456789.{ascii_letters}'

        if self.num_only:
            if self.int_only:
                valid_chars = valid_chars[:10]
            else:
                valid_chars = valid_chars[:11]

        for s in self.user_text:
            if s not in valid_chars:
                return False

        return True


    def reset_selection(self):
        self.selected = False
        self.user_text = ''


    def render_text(self):
        self.text_render = self.text_render = self.text_font.render(f'{self.text}{self.text_suffix}', 1, self.text_colour)