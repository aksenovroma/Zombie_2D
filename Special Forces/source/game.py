from math import atan2, pi
from source.player import Player
from source.enemy import Enemy
from source.aim import Aim
from source.menu import Menu
from source.health_line import HPLine
from source.blood import Blood
from source.constants import *
from random import randrange
import pygame

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SET_1)

bg = pygame.image.load('bg_2.jpg')
menu_bg = pygame.image.load('menu-background.jpg')

menu_sound_2 = pygame.mixer.Sound('sounds\\button_click_2.wav')
menu_sound_2.set_volume(0.5)

shot_sound = pygame.mixer.Sound('sounds\shoot.wav')
shot_sound.set_volume(1)

move_sound = pygame.mixer.Sound('sounds\zombie_move.wav')
move_sound.set_volume(0.1)

attack_sound = pygame.mixer.Sound('sounds\zombie_attack.wav')
attack_sound.set_volume(0.2)


class Game:
    def __init__(self):
        self.man = Player('solder.png')
        self.aim = Aim('aim.png')
        self.menu = Menu('menu-background.jpg')
        self.hp_line = HPLine()
        self.blood = Blood()

        self.bloods = []
        self.zombies = []
        self.difficulty = DIFICULTY
        self.clock = pygame.time.Clock()
        self.font_score = pygame.font.Font(FONT, MAN_SCORE_TEXT_SIZE)
        self.font_go = pygame.font.Font(FONT, FONT_SIZE_GO)
        self.text = self.font_go.render(TEXT_GO, True, TEXT_COLOR)
        self.text_rect = self.text.get_rect()
        self.blood_GO = pygame.image.load('blood_GO.png')

    def render_game(self):
        text = self.font_score.render(MAN_SCORE_TEXT + str(self.man.score), True, MAN_SCORE_COLOR)
        win.blit(bg, (0, 0))
        win.blit(text, (5, 0))
        for i in self.bloods:
            if len(self.bloods) < MAX_BLOOD:
                self.blood.check_xy(i[0], i[1], i[2])
                self.blood.draw_blood(win)
            else:
                del self.bloods[0]
        self.man.draw(win)
        for x in self.zombies:
            x.draw(win)
        self.aim.draw(win)
        self.hp_line.draw(win)
        pygame.display.update()

    def render_menu(self):
        pygame.mouse.set_visible(True)
        menu_loop = True
        quite = False
        while menu_loop:
            self.clock.tick(20)

            pos = pygame.mouse.get_pos()
            but1 = self.menu.choose_1(pos[0], pos[1])
            but2 = self.menu.choose_2(pos[0], pos[1])

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and but1:
                        menu_sound_2.play()
                        return True

                    if event.button == 1 and but2:
                        menu_sound_2.play()
                        menu_loop = False
                        quite = True

                if event.type == pygame.QUIT:
                    menu_loop = False
                    quite = True

            self.menu.draw(win)
            pygame.display.update()

        if quite:
            pygame.quit()
        return False

    def turn_man(self, pos):
        self.man.angle = -(180 * atan2(pos[1] - self.man.rect.y, pos[0] - self.man.rect.x) / pi)

    def move_man(self, keys):
        if self.man.isRun:
            self.man.step *= 2

        if keys[pygame.K_a] and self.man.rect.x > -self.man.rect.width + self.man.step:
            self.man.rect.x -= self.man.step

        if keys[pygame.K_d] and self.man.rect.x < SCREEN_WIDTH - self.man.rect.width:
            self.man.rect.x += self.man.step

        if keys[pygame.K_w] and self.man.rect.y > -self.man.rect.height + self.man.step:
            self.man.rect.y -= self.man.step

        if keys[pygame.K_s] and self.man.rect.y < SCREEN_HEIGHT - self.man.rect.height:
            self.man.rect.y += self.man.step

        if keys[pygame.K_r] or self.man.bullets == 0:
            self.man.reload = True
            self.man.bullets = MAN_BULLETS

        self.man.isRun = False
        self.man.step = MAN_STEP * 2

        if keys[pygame.K_SPACE]:
            self.man.isRun = True

    def move_zombie(self, pos):
        for zombie in self.zombies:
            if zombie.go:
                zombie.move()
            if zombie.rect.x < 0 - zombie.rect.width:
                self.hp_line.change(HP_CHANGE)
                self.zombies.remove(zombie)

            if zombie.attack_man(self.man):
                self.man.health -= ZOMBIE_DAMAGE
                if self.man.health <= 0:
                    return False
                attack_sound.play()

            if self.man.shoot and zombie.check_shoot(pos[0], pos[1]):
                zombie.health -= MAN_DAMAGE
                if zombie.health < MAN_DAMAGE:
                    zombie.health = -1
                if not zombie.live:
                    zombie.go = False
                    self.man.score += 1
                    if 5 < self.man.score < 10:
                        self.difficulty = 2
                    elif self.man.score > 10:
                        self.difficulty = 3
                    die_pos = (zombie.rect.x, zombie.rect.y, randrange(0, 360))
                    self.bloods.append(die_pos)
                    self.zombies.remove(zombie)
        return True

    def add_zombie(self, timer):
        if len(self.zombies) < COUNT_OF_ZOMBIES:
            timer += 1
            if timer == DELAY:
                for i in range(self.difficulty):
                    self.zombies.append(Enemy('zombie.png'))
                timer = 0
        return timer

    def check_hp_line(self):
        if self.hp_line.width <= 0:
            return True

    def game_over(self):
        for i in range(TIMER):
            win.blit(self.blood_GO, (-30, 0))
            win.blit(self.text, (SCREEN_WIDTH/2 - self.text_rect.width/2, SCREEN_HEIGHT/2 - self.text_rect.height/2 - FONT_SIZE_GO/2))
            pygame.display.update()

    def start_game(self):
        pygame.mouse.set_visible(False)
        move_sound.play(-1)
        timer = 0

        game = True
        while game:
            self.clock.tick(20)

            keys = pygame.key.get_pressed()
            pos = pygame.mouse.get_pos()

            self.turn_man(pos)
            self.aim.move(pos[0], pos[1])

            if self.check_hp_line():
                game = False

            timer = self.add_zombie(timer)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.man.shoot = True
                        self.man.bullets -= 1
                        shot_sound.play()

            if not self.move_zombie(pos):
                game = False

            self.move_man(keys)

            self.man.shoot = False

            if keys[pygame.K_ESCAPE]:
                if self.render_menu():
                    pygame.mouse.set_visible(False)
                    continue
                else:
                    return False

            self.render_game()

        self.game_over()
        return True