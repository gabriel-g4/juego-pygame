import pygame
import COLORES
from FUNCIONES import *

class Hongo(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vivo = True
        self.vida = 100
        self.vida_maxima = self.vida

        self.speed = speed
        self.direccion = 1 # 1 derecha -1 izquierda
        self.flip = False

        self.actualizar_tiempo = pygame.time.get_ticks()
        self.accion = 0 # indice 0: idle 1: walk 2: ataque 3: morir
        self.accion_completa = False
        self.indice_fotograma = 0
        self.lista_animaciones = cargar_imagenes("IMAGENES\PERSONAJES\HONGO", ["idle", "walk", "ataque", "muerte"] , scale)
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.image.get_rect()
        
        self.rect.midbottom = (x, y)
        
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.GRAY)

    
    def actualizar(self):
        '''Metodo que llama a otros metodos que necesitan ser actualizados.'''
        self.actualizar_animacion()
        self.chequear_vida()


    def actualizar_animacion(self):
        '''Actualiza la animacion de la accion actual'''
        #cooldown animacion
        ANIMACION_CD = 155
        #actualizar imagen
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        if self.accion == 3:
            self.rect.center = (self.x, self.y-30)
        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.actualizar_tiempo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]):
            if self.accion != 3:
                self.accion_completa = True
                self.indice_fotograma = 0
            else:
                self.kill()
            
    
    def actualizar_accion(self, nueva_accion):
        '''Recibe por parametro la accion nueva y si es distinta a la actual, la actualiza si la animacion está completa. '''
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
            self.actualizar_accion(3)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)

    
