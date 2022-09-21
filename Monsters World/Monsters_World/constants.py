import pygame
pygame.init()

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Fonts
TITLE_FONT = pygame.font.Font(None, 130)
INSTRUCTION_FONT = pygame.font.Font(None, 50)

# Images
MAIN_MENU_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('images\\button.png'), (400, 100))
MAP_IMAGE = pygame.image.load('images\\MonsterWorldMap.png')