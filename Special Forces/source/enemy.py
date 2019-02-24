from source.constants import *
from math import atan2, pi
import random
import pygame


class Enemy:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = (SPAWN_POINT[random.randint(0, len(SPAWN_POINT) - 1)][0])
        self.rect.y = (SPAWN_POINT[random.randint(0, len(SPAWN_POINT) - 1)][1])

        self.step = ZOMBIE_STEP
        self.health = ZOMBIE_HEALTH
        self.angle = ZOMBIE_ANGLE
        self.zombieFrameCount = ZOMBIE_FRAME_COUNT
        self.zombieFrameCount_1 = ZOMBIE_FRAME_COUNT

        self.go = True
        self.live = True
        self.attack = False

        self.zombieAnim = []
        self.zombieAttackAnim = []

        self.__anim_move()
        self.__anim_attack()

    def __anim_attack(self):
        for i in range(ZOMBIE_ANIM_ATTACK):
            self.zombieAttackAnim.append(pygame.image.load('attack_zombie\skeleton-attack_' + str(i) + '.png'))

    def __anim_move(self):
        for i in range(ZOMBIE_ANIM_MOVE):
            self.zombieAnim.append(pygame.image.load('move_zombie\skeleton-move_' + str(i) + '.png'))

    def draw_anim_move(self, window):
        if self.zombieFrameCount > ZOMBIE_ANIM_MOVE:
            self.zombieFrameCount = 0

        if self.go or (self.rect.x < SCREEN_HEIGHT - self.rect.height or self.rect.y < SCREEN_WIDTH - self.rect.width):
            img = pygame.transform.rotate(self.zombieAnim[self.zombieFrameCount // 2], self.angle)
            window.blit(img, (self.rect.x, self.rect.y))
            self.zombieFrameCount += 1

    def draw_anim_attack(self, window):
        if self.zombieFrameCount > ZOMBIE_ANIM_ATTACK:
            self.zombieFrameCount = 0

        if self.go or (self.rect.x < SCREEN_HEIGHT - self.rect.height or self.rect.y < SCREEN_WIDTH - self.rect.width):
            img = pygame.transform.rotate(self.zombieAttackAnim[self.zombieFrameCount // 2], self.angle)
            window.blit(img, (self.rect.x, self.rect.y))
            self.zombieFrameCount += 1

    def attack_man(self, solder):
        solder_rect = (solder.rect.x, solder.rect.y, solder.rect.width - 20, solder.rect.height - 20)
        if self.rect.colliderect(solder_rect):
            self.attack = True
            self.angle = -(180 * atan2(solder.rect.y - self.rect.y, solder.rect.x - self.rect.x) / pi)
            self.step = 0
            return self.attack
        else:
            self.attack = False
            self.angle = ZOMBIE_ANGLE
            self.step = ZOMBIE_STEP
            return self.attack

    def check_shoot(self, x, y):
        if self.rect.x <= x <= self.rect.x + self.rect.width and \
        self.rect.y <= y <= self.rect.y + self.rect.height:
            self.dead()
            return True

    def draw(self, window):
        if self.live and self.attack:
            self.draw_anim_attack(window)
        elif self.live:
            self.draw_anim_move(window)
        if self.health >= 0:
            pygame.draw.rect(window, (255, 0, 0),
                         ((self.rect.width / 2 + self.rect.x, self.rect.height / 2 + self.rect.y), (self.health, 5)))

    def move(self):
        self.rect.x -= self.step
        if self.rect.x < -self.rect.width:
            self.live = False

    def dead(self):
        if self.health < 0:
            self.live = False
            return False
