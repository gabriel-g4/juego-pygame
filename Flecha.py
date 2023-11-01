from typing import Any
import pygame

class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y , direccion, flecha_imagen, flip):
        pygame.sprite.Sprite.__init__(self)
        self.direccion = direccion
        self.velocidad = 10
        self.image = flecha_imagen
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)

    def update(self):
        # mover flecha
        self.rect.x += (self.direccion * self.velocidad)