from typing import Any
import pygame
import COLORES
from CONSTANTES import *

class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y , direccion, flecha_imagen, flip):
        pygame.sprite.Sprite.__init__(self)
        self.direccion = direccion
        self.velocidad = 10

        self.actualizar_tiempo = pygame.time.get_ticks()
        
        self.image = flecha_imagen
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        

    def update(self, enemigo_grupo , grupo_flechas, mundo, screen_scroll):

        self.rect.x += screen_scroll

        # mover flecha
        self.rect.x += (self.direccion * self.velocidad)

        # fijarse si salio de pantalla
        if self.rect.left > ANCHO_VENTANA or self.rect.right < 0:
            self.kill()
    
        
        # chequear colisiones
        for tile in mundo.lista_obstaculos:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemigo in enemigo_grupo:
            if pygame.sprite.spritecollide(enemigo, grupo_flechas, False):
                if enemigo.vivo:
                    enemigo.vida -= 25
                    enemigo.actualizar_accion(2)
                    print(enemigo.vida)
                    self.kill()
                    

        

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)
