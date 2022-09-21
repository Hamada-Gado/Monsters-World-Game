import pygame, sys
from pygame.locals import *
from .constants import BLACK, INSTRUCTION_FONT, MAP_IMAGE, WHITE
pygame.init()

def _1P(screen: pygame.Surface, clock: pygame.time.Clock, fps: int):

    world = pygame.transform.scale(MAP_IMAGE, ((MAP_IMAGE.get_width()*800)//MAP_IMAGE.get_height(), 800))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        screen.blit(world, (0, 0))
        pygame.display.update()
        


def _2P(screen: pygame.Surface, clock: pygame.time.Clock, fps: int):

    world = MAP_IMAGE

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


def instruction_menu(screen: pygame.Surface, clock: pygame.time.Clock, fps: int):

    def write_instructions():
        with open('Monsters_World\\Instruction.txt', 'r') as instructions:
            instructions = instructions.read()
        instructions = instructions.split('\n')
        instruction = ''

        for num, line in enumerate(instructions):
            instruction = INSTRUCTION_FONT.render(line, True, WHITE)
            screen.blit(instruction, (padding, padding + spacing*num - scrolling_pos))

    spacing = 45
    padding = 20
    scrolling_pos = 0
    scrolling_speed = 15
    scrolling_limit = 10_000

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 4:
                    if scrolling_pos <= 0:
                        scrolling_pos = 0
                    else:
                        scrolling_pos -= scrolling_speed
                    
                if event.button == 5:
                    if scrolling_pos >= scrolling_limit:
                        scrolling_pos = scrolling_limit
                    else:
                        scrolling_pos += scrolling_speed
            

        screen.fill(BLACK)
        write_instructions()
        pygame.display.update()
        clock.tick(fps)