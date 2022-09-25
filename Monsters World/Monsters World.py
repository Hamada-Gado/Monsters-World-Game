import pygame, sys
from pygame.locals import *
from Monsters_World.button import Button
from Monsters_World.menus import _1P, _2P, instruction_menu, choose_level
from Monsters_World.constants import MAIN_MENU_BUTTON_IMAGE, WHITE, TITLE_FONT, BLACK, GREY, MAP_IMAGE
from Monsters_World.game import Game
pygame.init()


SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
pygame.display.set_caption('Monsters World')
CLOCK = pygame.time.Clock()
FPS = 30



def main():
    game = Game(SCREEN, CLOCK, FPS)

    title = TITLE_FONT.render('Monsters World', True, BLACK, GREY)

    _1p_button = Button(MAIN_MENU_BUTTON_IMAGE, game.screen.get_width()//2, 320, '1P')
    _2p_button = Button(MAIN_MENU_BUTTON_IMAGE, game.screen.get_width()//2, 440, '2P')
    _2p_button.enable = False
    instruction_button = Button(MAIN_MENU_BUTTON_IMAGE, game.screen.get_width()//2, 560, 'INSTRUCTION')
    level_button = Button(MAIN_MENU_BUTTON_IMAGE, game.screen.get_width()//2, 680, 'LEVEL')
    quit_button = Button(MAIN_MENU_BUTTON_IMAGE, game.screen.get_width()//2, 800, 'QUIT')

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE) or (event.type == MOUSEBUTTONUP and quit_button.check_for_hovering(pos)):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if _1p_button.check_for_hovering(pos):
                    return _1P(game)
                if _2p_button.check_for_hovering(pos):
                    return _2P(game)
                if instruction_button.check_for_hovering(pos):
                    instruction_menu(game)
                if level_button.check_for_hovering(pos):
                    choose_level(game)

        game.screen.fill(WHITE)
        game.screen.blit(title, ((game.screen.get_width() - title.get_width())//2, 70))
        _1p_button.update(game.screen, pos)
        _2p_button.update(game.screen, pos)
        instruction_button.update(game.screen, pos)
        level_button.update(game.screen, pos)
        quit_button.update(game.screen, pos)
        pygame.display.update()
        game.clock.tick(game.fps)
           


if __name__ == '__main__':
    main()