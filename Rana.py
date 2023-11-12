import pygame
import random
import COLORES
from CONSTANTES import *
from FUNCIONES import *
from Proyectil import Proyectil

class Rana(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente, jugador) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.jugador = jugador
        self.x = x
        self.y = y
        self.vivo = True
        self.vida = 100
        self.vida_maxima = self.vida
        self.x = x
        self.y = y

        self.velocidad_y = 0
        self.speed = speed
        self.contador_movimiento = 0
        self.idle = False
        self.idle_contador = 0
        self.direccion = 1 # 1 derecha -1 izquierda
        self.flip = False
        self.atacando = False

        

        self.actualizar_tiempo = pygame.time.get_ticks()
        self.accion = 0 # 0: idle 1: walk 2: daño 3: ataque 4: lanzar 5: muerte
        self.accion_completa = False
        self.indice_fotograma = 0
        self.lista_animaciones = cargar_imagenes("IMAGENES\PERSONAJES\RANA", ["idle", "walk", "daño","ataque","ataque lanzar", "muerte"] , scale)
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.image.get_rect()
        
        self.rect.center = (x, y)
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.GRAY)

        self.rect_vision = pygame.Rect(0,0,200,self.rect.h)

        self.imagen_proyectil = pygame.image.load(r"IMAGENES\PROPS\proyectil.png").convert_alpha()
        self.imagen_proyectil = pygame.transform.scale_by(self.imagen_proyectil, 2)
        

    
    def actualizar(self, grupo_proyectiles):
        '''Metodo que llama a otros metodos que necesitan ser actualizados.'''
        self.actualizar_animacion()
        self.chequear_vida()
        if self.accion == 4 and self.accion_completa:
            proyectil = Proyectil(self.rect.centerx + ((10) * self.direccion), self.rect.centery, self.direccion, self.imagen_proyectil, self.flip)
            grupo_proyectiles.add(proyectil)
            self.accion_completa = False
            self.actualizar_accion(0)
    
    def moverse(self, movimiento_izq: bool, movimiento_der: bool, mundo):
        #reseteo  variables de movimiento
        dx = 0
        dy = 0

        #asignar movmiento
        if movimiento_izq:
            dx = -self.speed
            self.flip = True
            self.direccion = -1

        elif movimiento_der:
            dx = self.speed
            self.flip = False
            self.direccion = 1
            
        #colision con los tiles en x e y
        self.en_aire = True
        for tile in mundo.lista_obstaculos:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.w, self.rect.h):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.w, self.rect.h):
                if self.velocidad_y < 0: # saltando
                    self.velocidad_y = 0
                    dy = tile[1].bottom - self.rect.top
                
                elif self.velocidad_y >= 0:
                    self.velocidad_y = 0
                    self.en_aire = False
                    dy = tile[1].top - self.rect.bottom
        
        
        #aplicar gravedad
        if self.en_aire:
            self.velocidad_y += GRAVEDAD
            if self.velocidad_y > 10:
                self.velocidad_y = 10

        dy += self.velocidad_y
        
        #mover rectangulo
        self.rect.x += dx
        self.rect.y += dy

        
    def inteligencia(self, mundo):
        if self.vivo:
            # si rect de vision colisiona con jugador, disparar
            if self.rect_vision.colliderect(self.jugador.rect):
                self.actualizar_accion(4)
                self.atacando = True
            elif self.accion_completa:
                self.atacando = False
            
            if not self.atacando:
                # numero random para quedarse quieto
                if random.randint(1,400) == 7 and not self.idle:
                    self.actualizar_accion(0)
                    self.idle_contador = 0
                    self.idle = True

                if not self.idle:
                    self.actualizar_accion(1)

                    if self.direccion == 1:
                        movimiento_rana_der = True
                        movimiento_rana_izq = False
                    else:
                        movimiento_rana_der = False
                        movimiento_rana_izq = True

                    self.moverse(movimiento_rana_izq, movimiento_rana_der, mundo)
                    self.contador_movimiento += 1

                    self.rect_vision.center = (self.rect.centerx + 115 * self.direccion, self.rect.centery)
                    

                    if self.contador_movimiento > 50:
                        self.direccion *= -1
                        self.contador_movimiento *= -1
                elif self.idle:
                    self.idle_contador += 1
                    if self.idle_contador > 50:
                        self.idle = False

            


    def actualizar_animacion(self):
        '''Actualiza la animacion de la accion actual'''
        #cooldown animacion
        ANIMACION_CD = 155
        #actualizar imagen
        self.image = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect.w = self.image.get_rect().w
        self.rect.h = self.image.get_rect().h
        self.rect.h = self.rect.h - 7
        if self.accion == 5:
            self.rect.bottomleft = (self.rect.x , self.y + 30)

        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.actualizar_tiempo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]):
            if self.accion != 5:
                self.accion_completa = True
                self.indice_fotograma = 0
            else:
                self.kill()
            
    
    def actualizar_accion(self, nueva_accion):
        '''Recibe por parametro la accion nueva y si es distinta a la actual, la actualiza si la animacion está completa. 0: idle 1: walk 2: daño 3: ataque 4: lanzar 5: muerte'''
        # chequeo si hay una nueva accion y si termino la animacion o la animacion es CORRER necesito interrumpirla.
        if self.accion != nueva_accion and (self.accion_completa or self.accion == 1 or self.accion == 4):
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
            self.actualizar_accion(5)
        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)

    
