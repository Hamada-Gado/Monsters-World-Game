import pygame
pygame.init()

CARD_WIDTH = 200
CARD_HEIGHT = 100

BOX_SIZE = 45
X_MARGIN = 162
Y_MARGIN = 140

MOVE = 'move'
BATTLE = 'battle'
ROLL = 'roll'

START_ZONE = 'S'
ZORK_ZONE = 'Z'
VILLAGE_A = 'A'
VILLAGE_B = 'B'
VILLAGE_C = 'C'
NOT_ACCESSIBLE = 'N'

# DICE
DOT_RADIUS = 10
SPACING = 10

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
ROUND_BUTTON_GREEN = pygame.transform.scale(pygame.image.load('images\\round button green.png'), (170, 170))
ROUND_BUTTON_BLUE = pygame.transform.scale(pygame.image.load('images\\round button blue.png'), (170, 170))
ROUND_BUTTON_ORANGE = pygame.transform.scale(pygame.image.load('images\\round button orange.png'), (170, 170))
MAP_IMAGE = pygame.image.load('images\\MonsterWorldMap.png')

GOBLIN_IMAGE = pygame.transform.scale(pygame.image.load('images\\Goblin.png'), (CARD_WIDTH, CARD_HEIGHT))
GARGOYLE_IMAGE = pygame.transform.scale(pygame.image.load('images\\Gargoyle.png'), (CARD_WIDTH, CARD_HEIGHT))
DRAGON_IMAGE = pygame.transform.scale(pygame.image.load('images\\Dragon.png'), (CARD_WIDTH, CARD_HEIGHT))
ZORK_IMAGE = pygame.transform.scale(pygame.image.load('images\\Zork.png'), (CARD_WIDTH, CARD_HEIGHT))