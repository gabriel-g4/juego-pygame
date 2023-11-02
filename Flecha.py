from typing import Any
import pygame
import COLORES

class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y , direccion, flecha_imagen, flip, llegada):
        pygame.sprite.Sprite.__init__(self)
        self.direccion = direccion
        self.velocidad = 10
        self.tiempo_flecha = pygame.time.get_ticks()
        self.image = flecha_imagen
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        

    def update(self):
        # mover flecha
        self.rect.x += (self.direccion * self.velocidad)
        

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)
