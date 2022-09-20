import pygame, sys
from pygame.locals import *
from Monsters_World.button import Button
from Monsters_World.constants import MAIN_MENU_BUTTON, WHITE, TITLE_FONT, BLACK, GREY
pygame.init()

def main_menu(screen: pygame.Surface):

    title = TITLE_FONT.render('Monsters World', True, BLACK, GREY)

    _1p_button = Button(MAIN_MENU_BUTTON, 800, 300, '1P')
    _2p_button = Button(MAIN_MENU_BUTTON, 800, 450, '2P')
    instruction_button = Button(MAIN_MENU_BUTTON, 800, 600, 'INSTRUCTION')
    quit_button = Button(MAIN_MENU_BUTTON, 800, 750, 'QUIT')

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE) or (event.type == MOUSEBUTTONUP and quit_button.check_for_hovering(pos)):
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        screen.blit(title, (460, 100))
        _1p_button.update(screen, pos)
        _2p_button.update(screen, pos)
        instruction_button.update(screen, pos)
        quit_button.update(screen, pos)
        pygame.display.update()