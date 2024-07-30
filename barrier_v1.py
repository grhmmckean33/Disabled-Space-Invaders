import pygame
from pygame.sprite import Sprite

class Barrier(Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load('C:\\Users\\user\\Documents\\Python\\Invaders\\Ch11\\dbadge.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100  # Example health value
        self.original_image = self.image.copy()

    def take_damage(self, damage, bomb_rect):
        self.health -= damage
        if self.health <= 0:
            self.kill()
        else:
            self._update_image(bomb_rect)

    def _update_image(self, bomb_rect):
        # Create a mask where the bomb hit
        mask = pygame.Surface((bomb_rect.width, 3))
        mask.fill((0, 0, 0))  # Black color to simulate damage
        mask_rect = mask.get_rect(center=bomb_rect.center)
        self.image.blit(mask, mask_rect.topleft, special_flags=pygame.BLEND_RGBA_SUB)
