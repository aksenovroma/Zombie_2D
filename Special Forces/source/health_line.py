from source.constants import *
import pygame


class HPLine:
    def __init__(self):
        self.width = SCREEN_WIDTH - 10
        self.height = HP_LINE_HEIGHT
        self.color_line = (217, 127, 9)
        self.color_bg = (66, 66, 66)

    def draw(self, window):
        pygame.draw.rect(window, self.color_bg, ((0, SCREEN_HEIGHT - self.height - 10), (SCREEN_WIDTH, HP_LINE_HEIGHT + 10)))
        pygame.draw.rect(window, self.color_line, ((5, SCREEN_HEIGHT - self.height - 5), (self.width, self.height)))

    def change(self, damage):
        if self.width <= damage:
            self.width = 0
        else:
            self.width -= damage

