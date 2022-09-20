import pygame
pygame.init()

# Buttons
MAIN_MENU_BUTTON = pygame.transform.scale(pygame.image.load('images\\button.png'), (400, 100))

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Fonts
TITLE_FONT = pygame.font.Font(None, 130)