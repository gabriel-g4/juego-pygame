import os
import pygame
import COLORES
from CONSTANTES import *



class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.speed = speed
        self.velocidad_y = 0
        self.direccion = 1 # 1 derecha -1 izquierda
        self.salto = False
        self.en_aire = True
        self.flip = False
        self.lista_animaciones = []
        self.indice_fotograma = 0
        self.actualizar_tiempo = pygame.time.get_ticks()
        self.accion = 0 # es un indice
        self.accion_completa = False

        #cargar imagenes
        lista_animaciones = ["idle", "walk", "salto", "ataque"]
        for animacion in lista_animaciones:
            lista_temporal = []
            numero_frames = len(os.listdir(f"IMAGENES\PERSONAJES\DUENDA\{animacion}"))
            for i in range(numero_frames):
                img = pygame.image.load(f"IMAGENES\PERSONAJES\DUENDA\{animacion}\{i}.png").convert_alpha()
                img = pygame.transform.scale_by(img, scale)
                lista_temporal.append(img)
            self.lista_animaciones.append(lista_temporal)
        

        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.GRAY)
        

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
        PISO = 465
        if self.rect.bottom + dy > PISO:
            dy = PISO - self.rect.bottom
            self.en_aire = False

        #mover rectangulo
        self.rect.x += dx
        self.rect.y += dy



    def actualizar_animacion(self):
        #cooldown animacion
        ANIMACION_CD = 120
        #actualizar imagen
        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.actualizar_tiempo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]):
            self.accion_completa = True
            self.indice_fotograma = 0
            
    
    def actualizar_accion(self, nueva_accion):
        # chequeo si hay una nueva accion y si termino la animacion o la animacion es CORRER necesito interrumpirla.
        if self.accion != nueva_accion and (self.accion_completa or self.accion == 1):
            self.accion = nueva_accion
            #reseteo configuraciones de animacion
            self.indice_fotograma = 0
            self.accion_completa = False
            self.actualizar_tiempo = pygame.time.get_ticks()


    def dibujarse(self, screen):
        screen.blit(pygame.transform.flip(self.imagen, self.flip, False), (self.rect.x + 7, self.rect.y, self.rect.w, self.rect.h))
    
    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)
