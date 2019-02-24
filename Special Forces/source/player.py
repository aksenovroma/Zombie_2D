from source.constants import *
import pygame


class Player:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

        self.live = True
        self.isRun = False
        self.shoot = False
        self.reload = False

        self.step = MAN_STEP
        self.health = MAN_HEALTH
        self.manFrameCount = MAN_FRAME_COUNT
        self.angle = MAN_ANGLE
        self.bullets = MAN_BULLETS
        self.score = 0

        self.manAnim = []
        self.manAnimReload = []

        self.__anim_move()
        self.__anim_reload()

    def __anim_move(self):
        for i in range(MAN_ANIM_MOVE):
            self.manAnim.append(pygame.image.load('move\survivor-move_handgun_' + str(i) + '.png'))

    def __anim_reload(self):
        for i in range(MAN_ANIM_RELOAD):
            self.manAnimReload.append(pygame.image.load('man_reload_anim\survivor-reload_handgun_' + str(i) + '.png'))

    def __draw_anim_move(self, window):
        if self.manFrameCount > MAN_ANIM_MOVE:
            self.manFrameCount = 0

        if self.rect.x <= SCREEN_HEIGHT - self.rect.height or self.rect.y <= SCREEN_WIDTH - self.rect.width:
            img = pygame.transform.rotate(self.manAnim[self.manFrameCount // 2], self.angle)
            window.blit(img, (self.rect.x, self.rect.y))
            self.manFrameCount += 1
        else:
            window.blit(self.manAnim[0], (self.rect.x, self.rect.y))

    def __draw_anim_reload(self, window):
        img = pygame.transform.rotate(self.manAnimReload[self.manFrameCount//2], self.angle)
        window.blit(img, (self.rect.x, self.rect.y))
        self.manFrameCount += 1
        if self.manFrameCount > MAN_ANIM_RELOAD:
            self.manFrameCount = 0
            self.reload = False

    def draw(self, window):
        if self.reload:
            self.__draw_anim_reload(window)
        elif self.live:
            self.__draw_anim_move(window)
        pygame.draw.rect(window, (0, 255, 0),
                         ((self.rect.width/2 + self.rect.x, self.rect.height/2 + self.rect.y), (self.health, 5)))

