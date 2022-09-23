import pygame, sys
from pygame.locals import *
from .constants import BLACK, INSTRUCTION_FONT, MAP_IMAGE, ROUND_BUTTON_BLUE, ROUND_BUTTON_GREEN, ROUND_BUTTON_ORANGE, WHITE
from .game import Game
from .button import Button
pygame.init()

def _1P(game: Game):

    world = pygame.transform.scale(MAP_IMAGE, ((MAP_IMAGE.get_width()*800)//MAP_IMAGE.get_height(), 800))
    roll_button = Button(ROUND_BUTTON_ORANGE, game.screen.get_width() - ROUND_BUTTON_ORANGE.get_width()//2 - 50, 100, 'ROLL')

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                game.move_hero(event.pos)

                if roll_button.check_for_hovering(event.pos):
                    game.throw_dice()

        game.screen.fill('purple')
        game.screen.blit(world, (30, 30))
        roll_button.update(game.screen, pos)
        print(game.hero_dice)
        game.draw_hero(game.hero_pos)
        pygame.display.update()
        
        game.clock.tick(game.fps)
        


def _2P(game: Game):

    world = MAP_IMAGE

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


def instruction_menu(game: Game):

    def write_instructions():
        with open('Monsters_World\\Instruction.txt', 'r') as instructions:
            instructions = instructions.read()
        instructions = instructions.split('\n')
        instruction = ''

        for num, line in enumerate(instructions):
            instruction = INSTRUCTION_FONT.render(line, True, WHITE)
            game.screen.blit(instruction, (padding, padding + spacing*num - scrolling_pos))

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

            if event.type == KEYUP and event.key == K_BACKSPACE:
                return

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
            

        game.screen.fill(BLACK)
        write_instructions()
        pygame.display.update()
        game.clock.tick(game.fps)