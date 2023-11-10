import pygame
import COLORES
from CONSTANTES import *

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y , direccion, proyectil_imagen, flip):
        pygame.sprite.Sprite.__init__(self)
        self.direccion = direccion
        self.velocidad = 10

        self.actualizar_tiempo = pygame.time.get_ticks()
        
        self.image = proyectil_imagen
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        

    def update(self, jugador , grupo_proyectiles):
        
        # mover flecha
        self.rect.x += (self.direccion * self.velocidad)

        # fijarse si salio de pantalla
        if self.rect.left > ANCHO_VENTANA or self.rect.right < 0:
            self.kill()
    
        
        # chequear colisiones
        if pygame.sprite.spritecollide(jugador, grupo_proyectiles, False):
            if jugador.vivo:
                jugador.vida -= 1
                print(jugador.vida)
                self.kill()
                    

        

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)