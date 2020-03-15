import pygame as pg

class FontManager:

    def __init__(self):
        self.fonts = dict()

    def load(self, font_name, font_size):
        font_id = font_name + "," + str(font_size)
        if font_id not in self.fonts:
            self.fonts[font_id] = pg.font.SysFont(font_name, font_size)
        return self.fonts[font_id]