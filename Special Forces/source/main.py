from source.game import Game
import pygame

pygame.init()

pygame.display.set_caption("Special Forces")
icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

bg_music = pygame.mixer.Sound('sounds\\background_music.wav')
bg_music.set_volume(0.05)


def main():
    bg_music.play(-1)
    game = Game()
    flag = game.render_menu()
    while flag:
        if game.start_game():
            flag = game.render_menu()
            game = Game()
        else:
            flag = False


main()
