import os
import pygame
import constantes.COLORES as COLORES
from clases.Flecha import Flecha
from clases.Cuchillo import Cuchillo
from constantes.FUNCIONES import *
from constantes.CONSTANTES import *

pygame.mixer.init()

daño_duenda_efecto = pygame.mixer.Sound(r"SONIDO\daño duenda.wav")
daño_duenda_efecto.set_volume(0.2)






class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente, cantidad_cuchillos, score) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.vida = 3
        self.vida_maxima = self.vida
        self.fuente = fuente
        self.score = score

        self.cantidad_cuchillos = cantidad_cuchillos
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
        self.tiempo_inmunidad = 0
        self.tiempo_muerte = 0

        #cargar imagenes
        lista_nombres_animaciones = ["idle", "walk", "salto", "ataque", "muerte"]
        self.lista_animaciones = cargar_imagenes("img\PERSONAJES\DUENDA", lista_nombres_animaciones, scale)
        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.imagen.get_rect()

        self.rect.w = self.rect.w  - 15
        self.rect.h = self.rect.h - 10
        
        self.rect.center = (x, y)
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.RED1)

    

    def actualizar(self):
        '''Metodo que llama a otros metodos que necesitan ser actualizados.'''
        self.tiempo_inmunidad -= 1
        if self.tiempo_inmunidad <= 0:
            self.tiempo_inmunidad = 0

        self.actualizar_animacion()
        self.chequear_vida()
        


    def moverse(self, movimiento_izq: bool, movimiento_der: bool, mundo, fondo_scroll):
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
            self.velocidad_y = -17 # - 16
            self.salto = False
            self.en_aire = True

        #aplicar gravedad
        self.velocidad_y += GRAVEDAD
        if self.velocidad_y > 10:
            self.velocidad = 10

        dy += self.velocidad_y

        #colision con los tiles en x e y
        for tile in mundo.lista_obstaculos:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.w, self.rect.h):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.w, self.rect.h):
                if self.velocidad_y < 0: # saltando
                    self.velocidad_y = 0
                    dy = tile[1].bottom - self.rect.top
                
                elif self.velocidad_y >= 0: # quieto o cayendo
                    self.velocidad_y = 0
                    self.en_aire = False
                    dy = tile[1].top - self.rect.bottom

        # salir del mapa
        if self.rect.left + dx < 0 or self.rect.right + dx > ANCHO_VENTANA:
            dx = 0
        
        if self.rect.top > ALTO_VENTANA:
            self.rect.top = -50
            self.recibir_daño()
            self.velocidad_y = 3

        if self.rect.bottom < 0:
            dx = 0

        #mover rectangulo
        self.rect.x += dx
        self.rect.y += dy

        #scroll pantalla
        screen_scroll = 0
        if (self.rect.right > ANCHO_VENTANA - DISTANCIA_PARED_JUGADOR and fondo_scroll < COLUMNAS * TILE_SIZE - ANCHO_VENTANA)\
             or (self.rect.left < DISTANCIA_PARED_JUGADOR and fondo_scroll > 0):
            # si llega al limite de la pantalla, el personaje y la pantalla tienen que moverse hacia atras
            self.rect.x -= dx
            screen_scroll = -dx

        return screen_scroll



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
        if self.accion != nueva_accion and (self.accion_completa or self.accion == 1 or self.accion == 4):
            self.accion = nueva_accion
            #reseteo configuraciones de animacion
            self.indice_fotograma = 0
            self.accion_completa = False
            self.actualizar_tiempo = pygame.time.get_ticks()
    


    def action_handler(self, movimiento_izq, movimiento_der, mundo, grupo_flechas, grupo_cuchillo, fondo_scroll, flecha_imagen, ataque, lanzar_cuchillo):
        texto_cantidad_cuchillos = self.fuente.render(str(self.cantidad_cuchillos), True, COLORES.WHITE)
        if self.vivo:
            screen_scroll = self.moverse(movimiento_izq, movimiento_der, mundo, fondo_scroll)
            fondo_scroll -= screen_scroll

            if ataque:
                self.actualizar_accion(3) # 3: ataque
                if self.accion_completa:
                    flecha = Flecha((self.rect.centerx + (35 * self.direccion)), (self.rect.centery + 7), self.direccion, flecha_imagen, self.flip, self)
                    grupo_flechas.add(flecha) 
                    ataque = False
            elif lanzar_cuchillo and self.cantidad_cuchillos > 0:
                cuchillo = Cuchillo((self.rect.centerx + (35 * self.direccion)), (self.rect.centery + 7), self.direccion, self)
                grupo_cuchillo.add(cuchillo)
                lanzar_cuchillo = False
                self.cantidad_cuchillos -= 1
                texto_cantidad_cuchillos = self.fuente.render(str(self.cantidad_cuchillos), True, COLORES.WHITE)
                    
            if self.en_aire:
                self.actualizar_accion(2) # 2: saltar
                if ataque:
                    self.actualizar_accion(3) # 3: ataque
                    if self.accion_completa:
                        flecha = Flecha((self.rect.centerx + (35 * self.direccion)), (self.rect.centery + 7), self.direccion, flecha_imagen, self.flip, self)
                        grupo_flechas.add(flecha)
                        ataque = False
                elif lanzar_cuchillo and self.cantidad_cuchillos > 0:
                    cuchillo = Cuchillo((self.rect.centerx + (35 * self.direccion)), (self.rect.centery + 7), self.direccion, self)
                    grupo_cuchillo.add(cuchillo)
                    lanzar_cuchillo = False
                    self.cantidad_cuchillos -= 1
                    texto_cantidad_cuchillos = self.fuente.render(str(self.cantidad_cuchillos), True, COLORES.WHITE)
            elif movimiento_der or movimiento_izq:
                self.actualizar_accion(1) # 1: correr
            else:
                self.actualizar_accion(0) # 0: idle
        else:
            screen_scroll = self.moverse(False, False, mundo, fondo_scroll)
            self.tiempo_muerte += 1
        
        return screen_scroll, fondo_scroll, texto_cantidad_cuchillos, ataque, lanzar_cuchillo

    

    def recibir_daño(self):
        if self.tiempo_inmunidad <= 0 and self.vida > 0:
            daño_duenda_efecto.play()
            self.vida -= 1
            self.tiempo_inmunidad = 75
            print(self.vida)


    
    def chequear_vida(self):
        if self.vida <= 0:
            self.vida = 0
            self.speed = 0
            self.velocidad_y = 5
            self.vivo = False
            
            self.actualizar_accion(4)


    
    def dibujarse(self, screen):
        '''Blitea el personaje en pantalla en su rect.'''
        if self.vivo:
            if self.tiempo_inmunidad == 0 or self.tiempo_inmunidad >= 55 and self.tiempo_inmunidad <= 65 or self.tiempo_inmunidad >= 35 and self.tiempo_inmunidad <= 45\
            or self.tiempo_inmunidad >= 15 and self.tiempo_inmunidad <= 25 or self.tiempo_inmunidad <= 5:
                screen.blit(pygame.transform.flip(self.imagen, self.flip, False), (self.rect.x , self.rect.y, self.rect.w, self.rect.h))
        else:
            screen.blit(pygame.transform.flip(self.imagen, self.flip, False), (self.rect.x , self.rect.y, self.rect.w, self.rect.h))


    
    def dibujar_hitbox(self, screen):
        '''Blitea cuatro lineas separadoras que hacen de hitbox'''
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)

pygame.mixer.quit()
