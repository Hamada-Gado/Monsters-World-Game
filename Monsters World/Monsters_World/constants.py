import pygame
pygame.init()

CARD_WIDTH = 200
CARD_HEIGHT = 100

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)

# Fonts
TITLE_FONT = pygame.font.Font(None, 130)
INSTRUCTION_FONT = pygame.font.Font(None, 50)

# Images
MAIN_MENU_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('images\\button.png'), (400, 100))
MAP_IMAGE = pygame.image.load('images\\MonsterWorldMap.png')

GOBLIN_IMAGE = pygame.transform.scale(pygame.image.load('images\\Goblin.png'), (CARD_WIDTH, CARD_HEIGHT))
GARGOYLE_IMAGE = pygame.transform.scale(pygame.image.load('images\\Gargoyle.png'), (CARD_WIDTH, CARD_HEIGHT))
DRAGON_IMAGE = pygame.transform.scale(pygame.image.load('images\\Dragon.png'), (CARD_WIDTH, CARD_HEIGHT))
ZORK_IMAGE = pygame.transform.scale(pygame.image.load('images\\Zork.png'), (CARD_WIDTH, CARD_HEIGHT))