import pygame
pygame.init()

class Button:
    def __init__(self, image, x_pos, y_pos, text_input, font_text = "cambria", font_size = 50):
        self.font = pygame.font.SysFont(font_text, font_size)
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen, position):
        self.change_color(position)
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_hovering(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if self.check_for_hovering(position):
            self.text = self.font.render(self.text_input, True, "green")
        else:
            self.text = self.font.render(self.text_input, True, "white")
