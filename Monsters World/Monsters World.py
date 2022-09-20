import pygame, sys
from pygame.locals import *
from Monsters_World.menus import main_menu
pygame.init()


SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
pygame.display.set_caption('Monsters World')



def main():
    
    main_menu(SCREEN)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
           


if __name__ == '__main__':
    main()