import pygame
import os
import colores
from funciones import *
from constantes import *
#from Fantasma import *

on = True

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# VENTANA
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Mi primera chamba")

# FUENTE
fuente = pygame.font.SysFont("Arial", 20)
texto_coordenadas = fuente.render("", True, colores.WHITE)

# VARIABLES JUEGO

GRAVEDAD = 2.7

# VARIABLES JUGADOR

movimiento_izq = False
movimiento_der = False

#CLASES

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direccion = 1 # 1 derecha -1 izquierda
        self.flip = False

        img = pygame.image.load(r"IMAGENES\PERSONAJES\FANTASMA\ghost-idle\0.png")
        self.imagen = pygame.transform.scale_by(img, scale)
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        
    def dibujarse(self):
        screen.blit(self.imagen, self.rect)
    
    def dibujar_hitbox(self):

        pygame.draw.line(screen, colores.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, colores.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, colores.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, colores.RED1, self.rect.bottomright, self.rect.topright)
        

    

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed) -> None:
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

        #cargar imagenes
        lista_animaciones = ["idle", "walk", "salto"]
        for animacion in lista_animaciones:
            lista_temporal = []
            numero_frames = len(os.listdir(f"IMAGENES\PERSONAJES\DUENDA\{animacion}"))
            for i in range(numero_frames):
                img = pygame.image.load(f"IMAGENES\PERSONAJES\DUENDA\{animacion}\{i}.png")
                img = pygame.transform.scale_by(img, scale)
                lista_temporal.append(img)
            self.lista_animaciones.append(lista_temporal)
        

        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        self.rect = self.imagen.get_rect()
        #self.rect.center = (x, y)
        self.rect.width -= 55
        self.rect.height -= 24
        self.rect.x = (x)
        self.rect.y = (y)
        self.rect_valor = fuente.render(str(self.rect), True, colores.GRAY)
        #self.rect.scale_by_ip(0.5)
        
        

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
            self.velocidad_y = -24
            self.salto = False
            self.en_aire = True

        #aplicar gravedad
        self.velocidad_y += GRAVEDAD
        if self.velocidad_y > 10:
            self.velocidad = 10

        dy += self.velocidad_y

        #colision con piso
        PISO = 460
        if self.rect.bottom + dy > PISO:
            dy = PISO - self.rect.bottom
            self.en_aire = False

        #mover rectangulo
        self.rect.x += dx
        self.rect.y += dy



    def actualizar_animacion(self):
        #cooldown animacion
        ANIMACION_CD = 150
        #actualizar imagen
        self.imagen = self.lista_animaciones[self.accion][self.indice_fotograma]
        #fijarse cuanto tiempo paso
        if pygame.time.get_ticks() - self.actualizar_tiempo > ANIMACION_CD:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.indice_fotograma += 1
        
        if self.indice_fotograma >= len(self.lista_animaciones[self.accion]):
            self.indice_fotograma = 0
    
    def actualizar_accion(self, nueva_accion):
        
        if self.accion != nueva_accion:
            self.accion = nueva_accion
            #reseteo configuraciones de animacion
            self.indice_fotograma = 0
            self.actualizar_tiempo = pygame.time.get_ticks()



    def dibujarse(self):
        screen.blit(pygame.transform.flip(self.imagen, self.flip, False), (self.rect.left-30, self.rect.top-8, self.rect.width, self.rect.height))

    def dibujar_hitbox(self):

        pygame.draw.line(screen, colores.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, colores.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, colores.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, colores.RED1, self.rect.bottomright, self.rect.topright)


#IMAGENES

lista_fondos = []
for i in range (1,6):
    path = r"IMAGENES\FONDO\plx-"+ str(i) + ".png"
    fondo = pygame.image.load(path)
    fondo = pygame.transform.scale_by(fondo , 2.3)
    lista_fondos.append(fondo)


estructuras = pygame.image.load(r"IMAGENES\estructuras2.png")
estructuras = pygame.transform.scale_by(estructuras, 1)

#Eventos usuario

timer = pygame.USEREVENT
pygame.time.set_timer(timer, 130)

fantasma = Fantasma(200, 200, 2, 10)
jugador = Jugador(300, 300, 1.6, 10)


while on:

    clock.tick(FPS)

    lista_eventos = pygame.event.get()
    #######################EVENTOS###########################
    for evento in lista_eventos:

        # quit
        if evento.type == pygame.QUIT:
            on = False
        
        # mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            coordenadas_click = list(evento.pos)
            texto_coordenadas = fuente.render(str(coordenadas_click), True, colores.WHITE)
            print(coordenadas_click)

        # presion tecla
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                on = False
            if evento.key == pygame.K_a:
                movimiento_izq = True
            if evento.key == pygame.K_d:
                movimiento_der = True
            if evento.key == pygame.K_w and jugador.vivo:
                jugador.salto = True

        # levantamiento tecla
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                movimiento_izq = False
            if evento.key == pygame.K_d:
                movimiento_der = False
        elif evento.type == pygame.USEREVENT:
            pass


    lista_presiones = pygame.key.get_pressed()
    if True in lista_presiones:
        if lista_presiones[pygame.K_RIGHT]:
            pass

        elif lista_presiones[pygame.K_LEFT]:
            pass
    if lista_presiones[pygame.K_RIGHT] is False and lista_presiones[pygame.K_LEFT] is False:
        pass
    

    ##############PANTALLA############################
    for fondo in lista_fondos:
        screen.blit(fondo, (0, 0))

    screen.blit(estructuras, (0,0))
    screen.blit(texto_coordenadas, POS_COORD)

    jugador.actualizar_animacion()
    
    jugador.moverse(movimiento_izq, movimiento_der)
    
    #actualizar acciones
    if jugador.vivo: 
        if jugador.en_aire:
            jugador.actualizar_accion(2) # 2: saltar
        elif movimiento_der or movimiento_izq:
           jugador.actualizar_accion(1) # 1: correr
        else:
            jugador.actualizar_accion(0) # 0: idle


    screen.blit(jugador.rect_valor, (100, 0))
    screen.blit(fuente.render(str(jugador.rect.x), True, colores.ALICEBLUE), (0, 30))
    screen.blit(fuente.render(str(jugador.rect.y), True, colores.ALICEBLUE), (0, 60))
    screen.blit(fuente.render(str(jugador.rect.w), True, colores.ALICEBLUE), (0, 90))
    screen.blit(fuente.render(str(jugador.rect.h), True, colores.ALICEBLUE), (0, 120))

    pygame.draw.rect(screen, colores.AZURE1, fantasma.rect)
    fantasma.dibujarse()
    fantasma.dibujar_hitbox()

    pygame.draw.rect(screen, colores.AZURE1, jugador.rect)
    jugador.dibujarse()
    jugador.dibujar_hitbox()
    
    
    pygame.display.flip()

pygame.quit()