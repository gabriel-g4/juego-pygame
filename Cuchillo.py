import pygame
import os
import COLORES

from FUNCIONES import *
from CONSTANTES import *

class Cuchillo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.direccion = direccion
        self.velocidad = 4
        self.velocidad_y = -18
        self.tiempo_cuchillo = pygame.time.get_ticks()
        self.accion = 0 # solo tiene una
        self.indice_fotograma = 0
        

        self.lista_animaciones = cargar_imagenes("IMAGENES\PROPS", ["cuchillo"], 2.5)
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.image.get_rect()
        self.rect.center = (x ,y)


    def update(self, grupo_enemigos, grupo_cuchillos, mundo, screen_scroll):
        self.rect.x += screen_scroll

        # mover cuchillo
        self.movimiento()

        # actualizar animacion
        self.actualizar_animacion()

        # fijarse si salio de pantalla
        if self.rect.left > ANCHO_VENTANA or self.rect.right < 0:
            self.kill()
        
        # fijarse si toco el suelo
        for tile in mundo.lista_obstaculos:
            if tile[1].colliderect(self.rect):
                self.kill()
            if tile[1].colliderect(self.rect):
                self.kill()

        # chequear colisiones
        for enemigo in grupo_enemigos:
            if pygame.sprite.spritecollide(enemigo, grupo_cuchillos, False):
                if enemigo.vivo:
                    self.kill()
                    enemigo.actualizar_accion(2)
                    enemigo.vida -= 25
                    print(enemigo.vida)


    def movimiento(self):
        dx = 0
        dy = 0

        #aplicar gravedad
        self.velocidad_y += GRAVEDAD

        if self.velocidad_y > 10:
            self.velocidad_y = 10

        dy += self.velocidad_y
        dx += (self.velocidad * self.direccion)

        #colisoin con piso
        
        if self.rect.bottom + dy > PISO:
            dy = PISO - self.rect.bottom
            self.en_aire = False

        #mover rectangulo
        self.rect.x += dx
        self.rect.y += dy

    def actualizar_animacion(self):
        '''Actualiza la animacion de la accion actual'''
        #cooldown animacion
        ANIMACION_CD = 150
        #actualizar imagen
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.tiempo_cuchillo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]): 
            self.accion_completa = True
            self.indice_fotograma = 0

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)