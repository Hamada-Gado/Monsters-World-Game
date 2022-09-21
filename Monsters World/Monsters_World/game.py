import pygame
from .constants import RED
pygame.init()

class Game:
    hero_radius = 15

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, fps: int) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.hero_pos = (0, 0)
        self.create_world()

    def create_world(self):
        self.world = [['']*17]*14

        for x, y in ((-1,0), (-2,0), (-1,1), (-2,1)):
            self.world[x][y] = 's'
        for x, y in ((0,-4), (0,-5), (1,-5), (1,-4)):
            self.world[x][y] = 'z'

        self.world[12][7] = 'a'
        self.world[2][2] = 'b'
        self.world[5][-1] = 'c'

        not_accessible = ((2,0),(6,0),(4,1),(9,1),(10,1),(7,3),(10,3),(4,4),(13,4))

    def draw_hero(self, pos):
        self.hero_pos = pos
        pygame.draw.circle(self.screen, RED, self.hero_pos, Game.hero_radius)