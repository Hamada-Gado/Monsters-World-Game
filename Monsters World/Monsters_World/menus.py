import pygame, sys
from pygame.locals import *
from .constants import BATTLE, BLACK, BLUE, GAME_FONT, GREY, INSTRUCTION_FONT, MAIN_MENU_BUTTON_IMAGE, MAP_IMAGE, MOVE, PURPLE, ROLL, ROUND_BUTTON_ORANGE, TITLE_FONT, WHITE
from .game import Game
from .button import Button
pygame.init()

def _1P(game: Game):

    game.create_world()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                result = game.move_hero(event.pos)
                if result == False:
                    return lose_menu(game)
                elif result == True:
                    return win_menu(game)

                if game.roll_button.check_for_hovering(event.pos) and game.phase == ROLL:
                    game.throw_hero_dice()
                    if game.phase != BATTLE:
                        game.phase = MOVE
                        game.get_num_moves()

        game.update(pygame.mouse.get_pos())
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

def choose_level(game: Game):

    level1_button = Button(MAIN_MENU_BUTTON_IMAGE, 300, 300, 'Level 1: HP = 400')
    level2_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 300, 'Level 2: HP = 300')
    level3_button = Button(MAIN_MENU_BUTTON_IMAGE, 1300, 300, 'Level 3: HP = 200')
    return_button = Button(MAIN_MENU_BUTTON_IMAGE, 800, 500, 'RETURN')

    while True:

        if game.level == 1:
            level1_button.enable = False
        else:
            level1_button.enable = True
        
        if game.level == 2:
            level2_button.enable = False
        else:
            level2_button.enable = True

        if game.level == 3:
            level3_button.enable = False
        else:
            level3_button.enable = True

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:

                if level1_button.check_for_hovering(event.pos):
                    game.level = 1
                    game.hero_hit_points = 400

                if level2_button.check_for_hovering(event.pos):
                    game.level = 2
                    game.hero_hit_points = 300

                if level3_button.check_for_hovering(event.pos):
                    game.level = 3
                    game.hero_hit_points = 200

                if return_button.check_for_hovering(event.pos):
                    return

        game.screen.fill(WHITE)
        level1_button.update(game.screen, pygame.mouse.get_pos())
        level2_button.update(game.screen, pygame.mouse.get_pos())
        level3_button.update(game.screen, pygame.mouse.get_pos())
        return_button.update(game.screen, pygame.mouse.get_pos())    
        pygame.display.update()

        game.clock.tick(game.fps)

def lose_menu(game: Game):
    pass

def win_menu(game: Game):
    pass