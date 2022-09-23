from random import randint
import pygame
from .constants import BOX_SIZE, DOT_RADIUS, MOVE, NOT_ACCESSIBLE, RED, ROLL, SPACING, START_ZONE, VILLAGE_A, VILLAGE_B, VILLAGE_C, X_MARGIN, Y_MARGIN, ZORK_ZONE
pygame.init()

class Game:
    hero_radius = 15

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, fps: int) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.phase = None
        self.x, self.y = 16, 0
        self.hero_pos = self.center_coords_of_hero(self.x, self.y)
        self.hero_dice = [0, 0]
        self.zork_dice = [0, 0] 
        self.create_world()

    def create_world(self):
        self.world = [['' for y in range(14)] for x in range(17)]

        for x, y in ((-1,0), (-2,0), (-1,1), (-2,1)):
            self.world[x][y] = START_ZONE
        for x, y in ((0,-4), (0,-5), (1,-5), (1,-4)):
            self.world[x][y] = ZORK_ZONE

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

    def draw_hero(self, pos):
        self.hero_pos = pos
        pygame.draw.circle(self.screen, RED, self.hero_pos, Game.hero_radius)

    def move_hero(self, pos):
        # if self.phase != MOVE:
        #     return
        x, y , center = self.get_hero_at_pixel(pos[0], pos[1])
        if x == None or y == None or center == None or self.world[x][y] == NOT_ACCESSIBLE:
            return

        if self.hero_dice[0] != 0 and abs(self.x - x) == self.hero_dice[0] and self.y - y == 0:
            self.hero_dice[0] = 0
            self.x, self.y = x, y
            self.hero_pos = center
            return

        elif self.hero_dice[1] != 0 and abs(self.x - x) == self.hero_dice[1] and self.y - y == 0:
            self.hero_dice[1] = 0
            self.x, self.y = x, y
            self.hero_pos = center
            return

        elif self.hero_dice[0] != 0 and abs(self.y - y) == self.hero_dice[0] and self.x - x == 0:
            self.hero_dice[0] = 0
            self.x, self.y = x, y
            self.hero_pos = center
            return

        elif self.hero_dice[1] != 0 and abs(self.y - y) == self.hero_dice[1] and self.x - x == 0:
            self.hero_dice[1] = 0
            self.x, self.y = x, y
            self.hero_pos = center
            return
            

    def throw_dice(self):
        # if self.phase != ROLL:
        #     return
        self.hero_dice = [randint(1,6), randint(1,6)]
        if self.hero_dice[0] == 4:
            self.hero_dice[0] = 1
        elif self.hero_dice[0] == 5:
            self.hero_dice[0] = 2
        elif self.hero_dice[0] == 6:
            self.hero_dice[0] = 3

        if self.hero_dice[1] == 4:
            self.hero_dice[1] = 1
        elif self.hero_dice[1] == 5:
            self.hero_dice[1] = 2
        elif self.hero_dice[1] == 6:
            self.hero_dice[1] = 3

    def draw_die(self, num_dots, pos):

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

        pygame.draw.rect(self.screen, 'green', outer_frame)
        pygame.draw.rect(self.screen, 'black', inner_frame)
        for dot in dots:
            pygame.draw.circle(self.screen, 'red', dot.center, DOT_RADIUS)