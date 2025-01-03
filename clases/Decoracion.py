import pygame
from constantes.CONSTANTES import *

class Decoracion(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x  + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, screen_scroll):

        self.rect.x += screen_scroll