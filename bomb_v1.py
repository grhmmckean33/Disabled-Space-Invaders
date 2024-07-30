import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen

        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 0, 0))  # Red color for the bomb
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 5  # Speed of the bomb

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= self.screen.get_rect().bottom:
            self.kill()

    def draw_bomb(self):
        self.screen.blit(self.image, self.rect)
