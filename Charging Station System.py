# Jacob Meadows
# Practicum IT, 7th - 8th Period
# 05 September 2019
"""
Charging Station System for Practicum IT

Copyright (C) 2019 Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import pygame
import string
import motor_spin
import ID_Check


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Review")
        pygame.key.set_repeat(500, 20)
        self.window = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        self.texts = dict()
        self.buttons = dict()
        self.text_inputs = dict()
        self.menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.key_callback(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_callback(event)

            self.window.fill((0, 0, 0))
            for text_object in self.texts:
                self.texts[text_object].render(self.window)
            for button in self.buttons:
                self.buttons[button].render(self.window)
            for text_input in self.text_inputs:
                self.text_inputs[text_input].render(self.window)

            pygame.display.flip()
            self.clock.tick()

    def menu(self):
        self.texts["title"] = TextObject(text="Charging Station", rect=(0, 40, 1024, 60), fg_color=(0, 255, 0),
                                         justify="center", font=("Times New Roman", 80))
        self.texts["instructions"] = TextObject(text="Input 4 digit school ID and press enter", rect=(0, 200, 1024, 60),
                                                fg_color=(0, 255, 0), justify="center", font=("Times New Roman", 40))
        self.text_inputs["pin_input"] = TextInput(self, text="", rect=(467, 300, 90, 50), fg_color=(0, 255, 0),
                                                  restriction=string.digits, limit=4, command=self.code_input,
                                                  font=("Times New Roman", 40))
        self.text_inputs["pin_input"].focus_state = True

    def admin_menu(self):
        self.texts["title"] = TextObject(text="ADMIN MENU", rect=(0, 40, 1024, 60), fg_color=(0, 255, 0),
                                         justify="center", font=("Times New Roman", 80))
        self.texts["instructions"] = TextObject(
            text="1. Add User\n2. Delete User\n3. View All\n4. Exit Fullscreen\n5. Return to user menu",
            rect=(0, 150, 1024, 60), fg_color=(0, 255, 0), justify="center", font=("Times New Roman", 30)
        )

        def submit_command():  # todo add actual checking of code and user id
            if self.text_inputs['pin_input'].text == "1":
                pass
            elif self.text_inputs['pin_input'].text == "2":
                pass
            elif self.text_inputs['pin_input'].text == "3":
                pass
            elif self.text_inputs['pin_input'].text == "4":
                pass
            elif self.text_inputs["pin_input"].text == "5":
                self.menu()

        self.text_inputs["pin_input"] = TextInput(self, text="", rect=(497, 300, 30, 50), fg_color=(0, 255, 0),
                                                  restriction="1234", limit=1, command=submit_command,
                                                  font=("Times New Roman", 40))
        self.text_inputs["pin_input"].focus_state = True

    def code_input(self):
        if len(self.text_inputs['pin_input'].text) == 4:
            user_id = self.text_inputs["pin_input"].text
            self.text_inputs["pin_input"].text = ""
            self.text_inputs["pin_input"].limit = 6
            self.text_inputs["pin_input"].text_rect[0] -= 20
            self.text_inputs["pin_input"].rect[0] -= 20
            self.text_inputs["pin_input"].rect[2] = 130
            self.texts["instructions"].text = "Input 6 digit code and press enter"

            def submit_command():
                if len(self.text_inputs['pin_input'].text) == 6:
                    if user_id == "0000" and self.text_inputs['pin_input'].text == "123456":
                        self.admin_menu()
                    elif ID_Check.read(user_id, self.text_inputs['pin_input'].text):
                        self.open_command()
                    else:
                        self.menu()

            self.text_inputs["pin_input"].command = submit_command

    def open_command(self):
        self.buttons.clear()
        self.texts["title"].text = "OPEN"
        self.texts["instructions"].text = "Press Enter to close."
        self.text_inputs["pin_input"].fg_color = (0, 0, 0)

        def submit_command():
            motor_spin.close()
            self.menu()

        self.text_inputs["pin_input"].command = submit_command

        motor_spin.open()

    def key_callback(self, event):
        mods = pygame.key.get_mods()
        try:
            for text_input in self.text_inputs:
                self.text_inputs[text_input].key_input(event, mods)
        except RuntimeError:
            pass

    def mouse_button_callback(self, event):
        for button in self.buttons:
            if self.buttons[button].rect.collidepoint(event.pos):
                self.buttons[button].activate(self)
                break
        for text_input in self.text_inputs:
            if self.text_inputs[text_input].rect.collidepoint(*event.pos):
                self.text_inputs[text_input].focus_state = True
            else:
                self.text_inputs[text_input].focus_state = False


class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, rect=None):
        super().__init__()
        if image:
            if isinstance(image, str):
                self.image = pygame.image.load(image).convert()
            else:
                self.image = image
            if rect:
                self.rect = pygame.Rect(*rect[:2], *self.image.get_size())
            else:
                self.rect = self.image.get_rect()
        else:
            self.image = None
            if rect:
                self.rect = pygame.Rect(rect)
            else:
                self.rect = pygame.Rect(0, 0, 0, 0)
        self.dirty = True

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        return self.rect


class TextObject(Entity):
    def __init__(self, bg_color=(0, 0, 0), fg_color=(0, 0, 0), text=None, font=("Times New Roman", 20, False, False),
                 justify="left", width=0, enclosed=True, bg=True, **kwargs):
        super().__init__(**kwargs)
        self.font = pygame.font.SysFont(*font)
        self.bg_color = bg_color
        self.bg = bg
        self.fg_color = fg_color
        self.text = text
        self.text_rect = self.rect.copy()
        self.justify = justify
        self.width = width
        self.enclosed = enclosed
        self.cached_text = dict()
        self.formatted_text = list()

    def render(self, screen):
        if self.text is not None:
            if "{text}{fg_color}".format(text=self.text, fg_color=self.fg_color) not in self.cached_text:
                self.formatted_text = self.text.split("\n")
                text_line = 0
                while len(self.formatted_text) > text_line:
                    text_size = self.font.size(self.formatted_text[text_line])
                    new_line = " ".join(self.formatted_text[text_line].split()[:-1])
                    if self.enclosed:
                        while text_size[0] >= self.rect.width - 5:
                            new_line = " ".join(new_line.split()[:-1])
                            text_size = self.font.size(new_line)
                    if new_line != " ".join(self.formatted_text[text_line].split()[:-1]):
                        self.formatted_text.insert(text_line + 1, self.formatted_text[text_line][len(new_line) + 1:])
                        self.formatted_text[text_line] = self.font.render(
                            new_line, True, self.fg_color
                        )
                    else:
                        self.formatted_text[text_line] = self.font.render(
                            self.formatted_text[text_line], True, self.fg_color
                        )
                    text_line += 1
                self.cached_text["{text}{fg_color}".format(text=self.text, fg_color=self.fg_color)] = self.formatted_text[:]
            elif "{text}{fg_color}".format(text=self.text, fg_color=self.fg_color) in self.cached_text:
                self.formatted_text = self.cached_text["{text}{fg_color}".format(text=self.text, fg_color=self.fg_color)][:]
        if self.bg:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        if self.width > 0:
            pygame.draw.rect(screen, self.fg_color, self.rect, 1)
        if self.justify == "left":
            self.text_rect[0] += 5
        original_y = self.text_rect[1]
        self.text_rect[1] += 2
        if self.formatted_text:
            for text_line in range(len(self.formatted_text)):
                text_x = 0
                if self.justify == "center":
                    text_x = (self.text_rect[2] - self.formatted_text[text_line].get_width()) / 2
                self.text_rect[0] += text_x
                screen.blit(self.formatted_text[text_line], self.text_rect)
                self.text_rect[0] += self.formatted_text[text_line].get_width()
                if len(self.formatted_text) > text_line + 1:
                    self.text_rect[1] += self.formatted_text[text_line].get_height()
                self.text_rect[0] -= text_x + self.formatted_text[text_line].get_width()
            if self.justify == "left":
                self.text_rect[0] -= 5
            self.text_rect[1] = original_y
        super().update(screen)


class Button(TextObject):
    def __init__(self, command=None, focus_command=None, width=1, **kwargs):
        super().__init__(width=width, **kwargs)
        self.command = command
        self.focus_state_command = focus_command
        self.focus_state = False
        self.active_state = True

    def activate(self, given_object):
        if self.command is not None:
            try:
                self.command(given_object)
            except TypeError:
                self.command()

    def focus(self, pos):
        if self.focus_state_command is not None:
            self.focus_state_command(self, pos)


class TextInput(TextObject):
    def __init__(self, app, limit=0, restriction=None, command=None, width=1, **kwargs):
        super().__init__(width=width, **kwargs)
        self.app = app
        self.limit = limit
        self.restriction = restriction
        self.focus_state = False
        self.key_dict = {
            "`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(",
            "0": ")", "-": "_", "=": "+", "[": "{", "]": "}", ";": ":", "'": '"', "\\": "|", ",": "<", ".": ">",
            "/": "?"
        }
        self.active_ticks = 0
        self.active_state = True
        self.command = command

    def render(self, given_screen):
        super().render(given_screen)
        if self.focus_state:
            self.active_ticks += self.app.clock.get_time()
            if self.active_ticks / 1000 > 1:
                self.active_state = not self.active_state
                self.active_ticks %= 1000
            if self.active_state:
                given_screen.blit(
                    self.font.render("|", True, self.fg_color),
                    (self.text_rect[0] + sum([text_line.get_width() for text_line in self.formatted_text], 3),
                     self.text_rect[1])
                )
        else:
            self.active_state = False

    def key_input(self, event, mods):
        if self.focus_state:
            key_name = pygame.key.name(event.key).strip("[]")
            if len(self.text) < self.limit or self.limit == 0:
                if (self.restriction is not None and key_name in self.restriction) or self.restriction is None:
                    if key_name in string.ascii_letters:
                        if not mods & pygame.KMOD_LSHIFT:
                            self.text += key_name
                        elif mods & pygame.KMOD_LSHIFT:
                            self.text += key_name.upper()
                    elif key_name in self.key_dict:
                        if not mods & pygame.KMOD_LSHIFT:
                            self.text += key_name
                        elif mods & pygame.KMOD_LSHIFT:
                            self.text += self.key_dict[key_name]
                    elif key_name == "space":
                        self.text += " "
            if key_name == "backspace":
                self.text = self.text[:-1]
            elif key_name == "enter" or key_name == "return" and self.command is not None:
                self.command()


if __name__ == "__main__":
    App()
