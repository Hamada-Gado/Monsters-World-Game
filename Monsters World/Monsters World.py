import pygame, sys, os
from pygame.locals import *
from Monsters_World.button import Button
from Monsters_World.menus import _1P, _2P, instruction_menu
from Monsters_World.constants import MAIN_MENU_BUTTON_IMAGE, WHITE, TITLE_FONT, BLACK, GREY, MAP_IMAGE
from Monsters_World.game import Game
pygame.init()


SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
pygame.display.set_caption('Monsters World')
CLOCK = pygame.time.Clock()
FPS = 30



def main():
    title = TITLE_FONT.render('Monsters World', True, BLACK, GREY)

    _1p_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 300, '1P')
    _2p_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 450, '2P')
    instruction_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 600, 'INSTRUCTION')
    quit_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 750, 'QUIT')
    game = Game(SCREEN, CLOCK, FPS)

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE) or (event.type == MOUSEBUTTONUP and quit_button.check_for_hovering(pos)):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                if _1p_button.check_for_hovering(pos):
                    return _1P(game)
                if _2p_button.check_for_hovering(pos):
                    return _2P(game)
                if instruction_button.check_for_hovering(pos):
                    instruction_menu(game)

        game.screen.fill(WHITE)
        game.screen.blit(title, (460, 100))
        _1p_button.update(game.screen, pos)
        _2p_button.update(game.screen, pos)
        instruction_button.update(game.screen, pos)
        quit_button.update(game.screen, pos)
        pygame.display.update()
        game.clock.tick(game.fps)
           


if __name__ == '__main__':
    # os.chdir(os.path.join(os.path.dirname(sys.argv[0])))
    main()