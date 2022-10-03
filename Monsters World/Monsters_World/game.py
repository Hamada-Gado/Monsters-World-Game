from random import randint, choice
import pygame, sys
from pygame.locals import *
from .button import Button
from .constants import BATTLE, BLACK, BLUE, BOX_SIZE, DOT_RADIUS, DRAGON, GAME_FONT, GARGOYLE, GOBLIN, GREEN, GREY, HERO, HERO_IMAGE, MAP_IMAGE, MINES, MOVE, NOT_ACCESSIBLE, PURPLE, RED, ROLL, ROUND_BUTTON_ORANGE, SPACING, START_ZONE, VILLAGE_A, VILLAGE_B, VILLAGE_C, WHITE, X_MARGIN, Y_MARGIN, YELLOW, ZORK, MONSTERS, MONSTERS_NAMES
pygame.init()

class Game:
    hero_radius = 15

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, fps: int) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps

        self.level = 1
        self.hero_hit_points = 400
        self.moves = 0

        self.map = pygame.transform.scale(MAP_IMAGE, ((MAP_IMAGE.get_width()*800)//MAP_IMAGE.get_height(), 800)).convert_alpha()
        self.roll_button = Button(ROUND_BUTTON_ORANGE, self.screen.get_width() - ROUND_BUTTON_ORANGE.get_width()//2 - 50, ROUND_BUTTON_ORANGE.get_height()//2 + 30, 'ROLL')
        self.hero_hit_points_surface = GAME_FONT.render(f'HP: {self.hero_hit_points}', True, BLUE, WHITE)
        self.moves_surface = GAME_FONT.render(f'MOVES: {self.moves}', True, BLUE, WHITE)

    def create_world(self):

        self.phase = ROLL
        self.x, self.y = 16, 0
        self.hero_pos = self.center_coords_of_hero(self.x, self.y)
        self.zork_dice = [0, 0] 
        self.hero_dice = [0, 0]
        self.moves = 0

        self.world = [['' for y in range(14)] for x in range(17)]

        for x, y in ((-1,0), (-2,0), (-1,1), (-2,1)):
            self.world[x][y] = START_ZONE
        for x, y in ((0,-4), (0,-5), (1,-5), (1,-4)):
            self.world[x][y] = ZORK

        self.world[12][7] = VILLAGE_A
        self.world[2][2] = VILLAGE_B
        self.world[5][-1] = VILLAGE_C

        mountains = ((2,0),(6,0),(4,1),(9,1),(10,1),(7,3),(10,3),(4,4),(13,4),(4,5),(9,6),(12,6),(15,6),(16,6),(9,7),(5,8),(12,9),(11,10),(16,10),(4,11),(15,11),(6,13),(12,13))
        for x,y in mountains:
            self.world[x][y] = NOT_ACCESSIBLE

        empty = list((x,y) for x in range(2) for y in range(9))
        empty.extend([(2,6),(2,7),(2,8),(2,11),(2,12),(6,8),(6,9)])
        empty.extend([(x,y) for x in (7,8) for y in (0,1,5,6,7,8,9,10,13)])
        empty.extend([(9,0),(10,0),(11,0),(12,0),(13,0),(16,11),(14,12),(15,12),(16,12),(13,13),(14,13),(15,13),(16,13)])

        for x,y in empty:
            self.world[x][y] = NOT_ACCESSIBLE

        self.create_monsters()

    def create_monsters(self):
        goblins_num = MONSTERS[GOBLIN]['number']
        gargoyles_num = MONSTERS[GARGOYLE]['number']
        dragons_num = MONSTERS[DRAGON]['number']
        mines_num = MONSTERS[MINES]['number']
        monsters = [GOBLIN, GARGOYLE, DRAGON, MINES]


        total = goblins_num+gargoyles_num+dragons_num+mines_num
        i = 0
        while i < total:
            x, y = randint(0, len(self.world) - 1), randint(0, len(self.world[0]) - 1)
            if self.world[x][y] != '':
                continue
            if x != 0 and (self.world[x-1][y] in MONSTERS_NAMES or self.world[x-1][y] == MINES):
                continue
            if x != len(self.world)-1 and (self.world[x+1][y] in MONSTERS_NAMES or self.world[x+1][y] == MINES):
                continue
            if y != 0 and (self.world[x][y-1] in MONSTERS_NAMES or self.world[x][y-1] == MINES):
                continue
            if y != len(self.world[0])-1 and (self.world[x][y+1] in MONSTERS_NAMES or self.world[x][y+1] == MINES):
                continue
            monster = choice(monsters)
            if monster == GOBLIN:
                self.world[x][y] = GOBLIN
                goblins_num -= 1
                if goblins_num == 0:
                    monsters.remove(GOBLIN)
            elif monster == GARGOYLE:
                self.world[x][y] = GARGOYLE
                gargoyles_num -= 1
                if gargoyles_num == 0:
                    monsters.remove(GARGOYLE)
            elif monster == DRAGON:
                self.world[x][y] = DRAGON
                dragons_num -= 1
                if dragons_num == 0:
                    monsters.remove(DRAGON)
            elif monster == MINES:
                self.world[x][y] = MINES
                mines_num -= 1
                if mines_num == 0:
                    monsters.remove(MINES)
            i += 1

    def update(self, pos, color= PURPLE):
        self.hero_hit_points_surface = GAME_FONT.render(f'HP: {self.hero_hit_points}', True, BLUE, WHITE)
        self.moves_surface = GAME_FONT.render(f'MOVES: {self.moves}', True, BLUE, WHITE)

        self.screen.fill(color)
        self.screen.blit(self.map, (30, 30))
        self.screen.blit(self.moves_surface, (self.screen.get_width() - 500, self.screen.get_height() - 100))
        self.screen.blit(self.hero_hit_points_surface, (self.screen.get_width() - 500, self.screen.get_height() - self.moves_surface.get_height() - 100))
        self.roll_button.update(self.screen, pos)
        self.draw_die(self.hero_dice[0], (self.screen.get_width() - 400, 100), BLACK, GREEN, RED)
        self.draw_die(self.hero_dice[1], (self.screen.get_width() - 400, 230), BLACK, YELLOW, RED)
        self.draw_hero(self.hero_pos)

    def center_coords_of_hero(self, x, y):
        centerX = x * BOX_SIZE + X_MARGIN
        centerY = y * BOX_SIZE + Y_MARGIN
        return (centerX, centerY)

    def get_hero_at_pixel(self, x, y):
        for boxX in range(len(self.world)):
            for boxY in range(len(self.world[boxX])):
                center = self.center_coords_of_hero(boxX, boxY)
                boxRect = pygame.Rect(0, 0, BOX_SIZE, BOX_SIZE)
                boxRect.center = center
                if boxRect.collidepoint(x, y):
                    return (boxX, boxY, center)
        return (None, None, None)

    def draw_monsters(self):
        for x in range(17):
            for y in range(14):
                if self.world[x][y] == GOBLIN:
                    center = self.center_coords_of_hero(x, y)
                    pygame.draw.circle(self.screen, BLACK, center, Game.hero_radius)
                elif self.world[x][y] == GARGOYLE:
                    center = self.center_coords_of_hero(x, y)
                    pygame.draw.circle(self.screen, GREEN, center, Game.hero_radius)
                elif self.world[x][y] == DRAGON:
                    center = self.center_coords_of_hero(x, y)
                    pygame.draw.circle(self.screen, GREY, center, Game.hero_radius)
                elif self.world[x][y] == MINES:
                    center = self.center_coords_of_hero(x, y)
                    pygame.draw.circle(self.screen, BLUE, center, Game.hero_radius)             

    def draw_hero(self, pos):
        self.hero_pos = pos
        pygame.draw.circle(self.screen, RED, self.hero_pos, Game.hero_radius)

    def get_num_moves(self):
        if self.hero_dice[0] == 4:
            self.moves += 1
        elif self.hero_dice[0] == 5:
            self.moves += 2
        elif self.hero_dice[0] == 6:
            self.moves += 3
        else:
            self.moves += self.hero_dice[0]

        if self.hero_dice[1] == 4:
            self.moves += 1
        elif self.hero_dice[1] == 5:
            self.moves += 2
        elif self.hero_dice[1] == 6:
            self.moves += 3
        else:
            self.moves += self.hero_dice[1]


    def move_hero(self, pos):

        x, y , center = self.get_hero_at_pixel(pos[0], pos[1])
        if x == None or y == None or center == None or self.world[x][y] == NOT_ACCESSIBLE:
            return

        if self.world[self.x][self.y] == START_ZONE and self.world[x][y] == START_ZONE:
            self.x, self.y = x, y
            self.hero_pos = center

        if self.phase != MOVE:
            return

        if self.moves != 0 and abs(self.x - x) == 1 and self.y - y == 0:
            self.moves -= 1
            self.x, self.y = x, y
            self.hero_pos = center

        elif self.moves != 0 and abs(self.x - x) == 1 and self.y - y == 0:
            self.moves -= 1
            self.x, self.y = x, y
            self.hero_pos = center

        elif self.moves != 0 and abs(self.y - y) == 1 and self.x - x == 0:
            self.moves -= 1
            self.x, self.y = x, y
            self.hero_pos = center

        elif self.moves != 0 and abs(self.y - y) == 1 and self.x - x == 0:
            self.moves -= 1
            self.x, self.y = x, y
            self.hero_pos = center

        if self.world[self.x][self.y] == VILLAGE_A:
            self.hero_hit_points += 200
            self.flash(GREY, GREEN)
            self.world[self.x][self.y] = ''
        elif self.world[self.x][self.y] == VILLAGE_B:
            self.hero_hit_points += 150
            self.flash(GREY, GREEN)
            self.world[self.x][self.y] = ''
        elif self.world[self.x][self.y] == VILLAGE_C:
            self.hero_hit_points += 100
            self.flash(GREY, GREEN)
            self.world[self.x][self.y] = ''
        elif self.world[self.x][self.y] in MONSTERS_NAMES:
            if not self.battle(self.world[self.x][self.y]):
                return False
            self.world[self.x][self.y] = ''
        elif self.world[self.x][self.y] == MINES:
            self.flash(GREY, RED)
            self.hero_hit_points -= 100
        elif self.world[self.x][self.y] == ZORK:
            self.x, self.y = 0, 9
            self.hero_pos = self.center_coords_of_hero(self.x, self.y)
            self.moves = 0
            return self.battle(self.world[self.x][self.y])
            # return self.final_battle()
        
        if self.moves == 0:
            self.phase = ROLL

    def battle(self, monster_name: str):
        self.phase = ROLL
        self.map.set_alpha(128)
        turn = False
        monster_hp = MONSTERS[monster_name]['HP']

        while True:

            if self.hero_hit_points <= 0:
                self.map.set_alpha(255)
                self.phase = MOVE
                return False
            if monster_hp <= 0:
                pygame.time.wait(1000)
                self.throw_hero_dice()
                damage = self.hero_dice[0]*10 + self.hero_dice[1]
                self.hero_hit_points += damage
                self.flash(GREY, GREEN)
                self.map.set_alpha(255)
                self.phase = MOVE
                return True

            if turn == ZORK:
                pygame.time.wait(1000)
                self.throw_zork_dice()
                damage = self.zork_dice[0]*10 + self.zork_dice[1]
                self.flash(GREY, RED)
                self.hero_hit_points -= damage
                turn = HERO
           
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if self.roll_button.check_for_hovering(event.pos):
                        if turn == False:
                            self.throw_hero_dice(1)
                            self.throw_zork_dice(1)
                            if self.hero_dice[0] > self.zork_dice[0]:
                                turn = HERO
                            elif self.hero_dice[0] < self.zork_dice[0]:
                                pygame.time.wait(1000)
                                self.throw_zork_dice()
                                damage = self.zork_dice[0]*10 + self.zork_dice[1]
                                self.flash(GREY, RED)
                                self.hero_hit_points -= damage
                                turn = HERO
                            else:
                                turn = None
                        elif turn == HERO:
                            self.throw_hero_dice()
                            damage = self.hero_dice[0]*10 + self.hero_dice[1]
                            self.flash(GREY, BLUE)
                            monster_hp -= damage
                            if self.hero_dice[0] == self.hero_dice[1]:
                                self.flash(GREY, GREEN)
                                self.hero_hit_points += 100
                                monster_hp -= 100
                            turn = ZORK
                        elif turn == None:
                            self.throw_hero_dice()
                            self.throw_zork_dice()
                            self.flash(BLUE, RED)
                            damage = self.hero_dice[0]*10 + self.hero_dice[1]
                            if self.hero_dice[0] == self.hero_dice[1]:
                                self.hero_hit_points += 100
                                monster_hp -= 100
                            monster_hp -= damage

                            damage = self.zork_dice[0]*10 + self.zork_dice[1]
                            self.hero_hit_points -= damage
            

            if monster_hp < 0:
                monster_hp = 0
            if self.hero_hit_points < 0:
                self.hero_hit_points = 0
                
            monster_hit_points_surface = GAME_FONT.render(f'HP: {monster_hp}', True, RED, WHITE)

            self.update(pygame.mouse.get_pos())
            self.screen.blit(monster_hit_points_surface, (300, 200))
            self.draw_die(self.zork_dice[0], (self.screen.get_width() - 400, 400), BLACK, GREEN, RED)
            self.draw_die(self.zork_dice[1], (self.screen.get_width() - 400, 530), BLACK, YELLOW, RED)
            self.screen.blit(MONSTERS[monster_name]['image'], (300, 300))
            self.screen.blit(HERO_IMAGE, (550, 300))
            pygame.display.update()

            self.clock.tick(self.fps)

    def flash(self, color1, color2):
        for _ in range(10):
            color1, color2 = color2, color1
            self.update(pygame.mouse.get_pos(), color1)
            pygame.display.update()
            self.clock.tick(self.fps)

    def shuffle_dice(self, xOffset, y):
        for _ in range(50):

            die1 = randint(1, 6)
            die2 = randint(1, 6)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.draw_die(die1, (self.screen.get_width() - xOffset, y), BLACK, GREEN, RED)
            self.draw_die(die2, (self.screen.get_width() - xOffset, y + 130), BLACK, YELLOW, RED)
            pygame.display.update()

            self.clock.tick(self.fps)

        return [die1, die2]

    def throw_hero_dice(self, num_of_dice= 2):
        if self.phase != ROLL:
            return

        if num_of_dice == 2:
            self.hero_dice = self.shuffle_dice(400, 100)
        else:
            self.hero_dice = [self.shuffle_dice(400, 100)[0], 0]

    def throw_zork_dice(self, num_of_dice= 2):
        if self.phase != ROLL:
            return

        if num_of_dice == 2:
            self.zork_dice = self.shuffle_dice(400, 400)
        else:
            self.zork_dice = [self.shuffle_dice(400, 400)[0], 0]

    def draw_die(self, num_dots, pos, color_fg, color_bg, color_dot):

        inner_frame = pygame.Rect(0, 0, SPACING*4 + DOT_RADIUS * 2*3, SPACING*4 + DOT_RADIUS * 2*3)
        outer_frame = pygame.Rect(0, 0, inner_frame.w + 10, inner_frame.h + 10)
        outer_frame.center = pos
        inner_frame.center = pos
        dots = []
        if num_dots == 1:
            dot1 = pygame.Rect(0, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot1.center = inner_frame.center
            dots.append(dot1)
        elif num_dots == 2:
            dot1 = pygame.Rect(inner_frame.left + SPACING, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot1.centery = inner_frame.centery
            dot2 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot2.centery = inner_frame.centery
            dots.append(dot1)
            dots.append(dot2)
        elif num_dots == 3:
            dot1 = pygame.Rect(inner_frame.left + SPACING, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot2 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot3 = pygame.Rect(0, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot3.center = pos
            dots.append(dot1)
            dots.append(dot2)
            dots.append(dot3)
        elif num_dots == 4:
            dot1 = pygame.Rect(inner_frame.left + SPACING, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot2 = pygame.Rect(inner_frame.left + SPACING, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot3 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot4 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dots.append(dot1)
            dots.append(dot2)
            dots.append(dot3)
            dots.append(dot4)
        elif num_dots == 5:
            dot1 = pygame.Rect(inner_frame.left + SPACING, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot2 = pygame.Rect(inner_frame.left + SPACING, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot3 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot4 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot5 = pygame.Rect(0, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot5.center = pos
            dots.append(dot1)
            dots.append(dot2)
            dots.append(dot3)
            dots.append(dot4)
            dots.append(dot5)
        elif num_dots == 6:
            dot1 = pygame.Rect(inner_frame.left + SPACING, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot2 = pygame.Rect(inner_frame.left + SPACING, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot3 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.top + SPACING, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot4 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, inner_frame.bottom - SPACING - DOT_RADIUS * 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot5 = pygame.Rect(inner_frame.left + SPACING, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot5.centery = inner_frame.centery
            dot6 = pygame.Rect(inner_frame.right - SPACING - DOT_RADIUS * 2, 0, DOT_RADIUS * 2, DOT_RADIUS * 2)
            dot6.centery = inner_frame.centery
            dots.append(dot1)
            dots.append(dot2)
            dots.append(dot3)
            dots.append(dot4)
            dots.append(dot5)
            dots.append(dot6)

        pygame.draw.rect(self.screen, color_bg, outer_frame)
        pygame.draw.rect(self.screen, color_fg, inner_frame)
        for dot in dots:
            pygame.draw.circle(self.screen, color_dot, dot.center, DOT_RADIUS)