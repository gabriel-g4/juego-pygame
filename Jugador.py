import os
import pygame
import COLORES
from FUNCIONES import *
from CONSTANTES import *



class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.vida = 100
        self.vida_maxima = self.vida

        self.speed = speed
        self.velocidad_y = 0
        self.direccion = 1 # 1 derecha -1 izquierda
        self.salto = False
        self.en_aire = False
        self.flip = False
        self.lista_animaciones = []
        self.indice_fotograma = 0
        self.actualizar_tiempo = pygame.time.get_ticks()
        self.accion = 0 # es un indice
        self.accion_completa = False

        #cargar imagenes
        lista_nombres_animaciones = ["idle", "walk", "salto", "ataque", "muerte"]
        self.lista_animaciones = cargar_imagenes("DUENDA", lista_nombres_animaciones, scale)
        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.GRAY)

    
    def actualizar(self):
        '''Metodo que llama a otros metodos que necesitan ser actualizados.'''
        self.actualizar_animacion()
        self.chequear_vida()
        

    def moverse(self, movimiento_izq: bool, movimiento_der: bool):
        #reseteo  variables de movimiento
        dx = 0
        dy = 0

        #asignar movmiento
        if movimiento_izq:
            dx = -self.speed
            self.flip = True
            self.direccion = -1
        if movimiento_der:
            dx = self.speed
            self.flip = False
            self.direccion = 1
        
        #salto
        if self.salto == True and self.en_aire == False:
            self.velocidad_y = -16
            self.salto = False
            self.en_aire = True

        #aplicar gravedad
        self.velocidad_y += GRAVEDAD
        if self.velocidad_y > 10:
            self.velocidad = 10

        dy += self.velocidad_y

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
        ANIMACION_CD = 120
        #actualizar imagen
        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.actualizar_tiempo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]):
            if self.accion != 4:
                self.accion_completa = True
                self.indice_fotograma = 0
            else:
                self.indice_fotograma = len(self.lista_animaciones[self.accion]) - 1
    
    def actualizar_accion(self, nueva_accion):
        '''Recibee por parametro la accion nueva y si es distinta a la actual, la actualiza si la animacion está completa. '''
        # chequeo si hay una nueva accion y si termino la animacion o la animacion es CORRER necesito interrumpirla.
        if self.accion != nueva_accion and (self.accion_completa or self.accion == 1):
            self.accion = nueva_accion
            #reseteo configuraciones de animacion
            self.indice_fotograma = 0
            self.accion_completa = False
            self.actualizar_tiempo = pygame.time.get_ticks()

    def chequear_vida(self):
        if self.vida <= 0:
            self.vida = 0
            self.speed = 0
            self.vivo = False
            self.actualizar_accion(4)


    def dibujarse(self, screen):
        '''Blitea el personaje en pantalla en su rect.'''
        screen.blit(pygame.transform.flip(self.imagen, self.flip, False), (self.rect.x + 7, self.rect.y, self.rect.w, self.rect.h))
    
    def dibujar_hitbox(self, screen):
        '''Blitea cuatro lineas separadoras que hacen de hitbox'''
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)
