import pygame


class Blood:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

    def check_xy(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw_blood(self, window):
        img = pygame.transform.rotate(pygame.image.load('blood.png'), self.angle)
        window.blit(img, (self.x + 30, self.y + 30))


