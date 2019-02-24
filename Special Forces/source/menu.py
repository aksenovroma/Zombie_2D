from source.constants import *
import pygame


class Menu:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.text_color1 = TEXT_COLOR
        self.text_color2 = TEXT_COLOR
        self.button_choice_1 = False
        self.button_choice_2 = False

        self.text1 = self.font.render(TEXT_1, True, self.text_color1)
        self.rect1 = self.text1.get_rect()
        self.text2 = self.font.render(TEXT_2, True, self.text_color2)
        self.rect2 = self.text2.get_rect()

        self.sound_1 = pygame.mixer.Sound('sounds\\button_click_1.wav')
        self.sound_1.set_volume(0.1)

        self.rect1.x, self.rect1.y = (SCREEN_WIDTH/2-self.rect1.width/2, SCREEN_HEIGHT/2-self.rect1.height - FONT_SIZE)
        self.rect2.x, self.rect2.y = (SCREEN_WIDTH/2-self.rect2.width/2, SCREEN_HEIGHT/2-FONT_SIZE/1.1)

    def draw(self, window):
        self.text1 = self.font.render(TEXT_1, True, self.text_color1)
        self.text2 = self.font.render(TEXT_2, True, self.text_color2)

        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.text1, (self.rect1.x, self.rect1.y))
        window.blit(self.text2, (self.rect2.x, self.rect2.y))

    def choose_1(self, x, y):
        if self.rect1.x <= x <= self.rect1.x + self.rect1.width and \
            self.rect1.y <= y <= self.rect1.y + self.rect1.height:
            self.text_color1 = TEXT_COLOR_CHOOSE
            if not self.button_choice_1:
                self.sound_1.play()
                self.button_choice_1 = True
            return True
        else:
            self.text_color1 = TEXT_COLOR
            self.button_choice_1 = False


    def choose_2(self, x, y):
        if self.rect2.x <= x <= self.rect2.x + self.rect2.width and \
            self.rect2.y <= y <= self.rect2.y + self.rect2.height:
            self.text_color2 = TEXT_COLOR_CHOOSE
            if not self.button_choice_2:
                self.sound_1.play()
                self.button_choice_2 = True
            return True
        else:
            self.text_color2 = TEXT_COLOR
            self.button_choice_2 = False
