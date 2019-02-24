import pygame


class Aim:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, x, y):
        self.x = x - self.rect.height/2
        self.y = y - self.rect.width/2
