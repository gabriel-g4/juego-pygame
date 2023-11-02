import pygame
import os
import COLORES
from FUNCIONES import *
from CONSTANTES import *
from Fantasma import Fantasma
from Jugador import Jugador
from Flecha import Flecha

on = True

pygame.init()

# FRAMERATE

clock = pygame.time.Clock()
FPS = 60

# VENTANA
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Mi primera chamba")

# FUENTE
fuente = pygame.font.SysFont("Arial", 20)
texto_coordenadas = fuente.render("", True, COLORES.WHITE)

# VARIABLES DE JUEGO

GRAVEDAD = GRAVEDAD
CD_FLECHAS = 100
coordenadas_click = [0, 0]

# VARIABLES DE JUGADOR

movimiento_izq = False
movimiento_der = False
ataque = False

# IMAGEN FLECHA: la cargo aca para que sea siempre la misma y no cargarla cada vez que se dispara.

flecha_imagen = pygame.image.load(r"IMAGENES\PROPS\flecha.png").convert_alpha()
flecha_imagen = pygame.transform.scale_by(flecha_imagen, 1.6)

# grupos sprite

grupo_flechas = pygame.sprite.Group()

#IMAGENES

lista_fondos = []
for i in range (1,6):
    path = r"IMAGENES\FONDO\plx-"+ str(i) + ".png"
    fondo = pygame.image.load(path).convert_alpha()
    fondo = pygame.transform.scale_by(fondo , 2.3)
    lista_fondos.append(fondo)

estructuras = pygame.image.load(r"IMAGENES\estructuras2.png").convert_alpha()
estructuras = pygame.transform.scale_by(estructuras, 1)

#Eventos usuario

timer = pygame.USEREVENT
pygame.time.set_timer(timer, 130)

fantasma = Fantasma(580, 420, 2, 5, fuente)
jugador = Jugador(215, 425, 1.6, 5, fuente)

debug_mode = False
mouse_up = True


while on:

    clock.tick(FPS)

    lista_eventos = pygame.event.get()
    #######################EVENTOS###########################
    for evento in lista_eventos:

        # quit
        if evento.type == pygame.QUIT:
            on = False
        
        # mouse click
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            
            if evento.button == 1:

                coordenadas_click = list(evento.pos)
                texto_coordenadas = fuente.render(str(coordenadas_click), True, COLORES.WHITE)
                print(coordenadas_click)

                mouse_up = False
                ataque = True
                atacando = True
        
        # mouse up
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                mouse_up = True


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
            
            # modo debug con P
            if evento.key == pygame.K_p:
                if debug_mode is False:
                    debug_mode = True
                else:
                    debug_mode = False

        # levantamiento tecla
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                movimiento_izq = False
            if evento.key == pygame.K_d:
                movimiento_der = False
            
        
        # eventos de usuario
        elif evento.type == pygame.USEREVENT:
            pass

    ##############PANTALLA############################
    for fondo in lista_fondos:
        screen.blit(fondo, (0, 0))

    screen.blit(estructuras, (0,0))
    screen.blit(texto_coordenadas, POS_COORD)
    

    jugador.actualizar_animacion()
    
    jugador.moverse(movimiento_izq, movimiento_der)

    if mouse_up and jugador.accion == 3 and not atacando:
        ataque = False

        
    #actualizar acciones
    if jugador.vivo: 
        if ataque:
            jugador.actualizar_accion(3) # 3: ataque
            if jugador.accion_completa:
                flecha = Flecha((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion, flecha_imagen, jugador.flip, coordenadas_click)
                grupo_flechas.add(flecha)
                jugador.accion_completa = False
                atacando = False

        if jugador.en_aire:
            jugador.actualizar_accion(2) # 2: saltar
            if ataque:
                jugador.actualizar_accion(3) # 3: ataque
                if jugador.accion_completa:
                    flecha = Flecha((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion, flecha_imagen, jugador.flip, coordenadas_click)
                    grupo_flechas.add(flecha)
                    jugador.accion_completa = False
                    atacando = False

        elif movimiento_der or movimiento_izq:
           jugador.actualizar_accion(1) # 1: correr
        elif not ataque:
            jugador.actualizar_accion(0) # 0: idle


    if debug_mode:
        screen.blit(jugador.rect_valor, (100, 0))
        screen.blit(fuente.render(str(jugador.rect.x), True, COLORES.ALICEBLUE), (0, 30))
        screen.blit(fuente.render(str(jugador.rect.y), True, COLORES.ALICEBLUE), (0, 60))
        screen.blit(fuente.render(str(jugador.rect.w), True, COLORES.ALICEBLUE), (0, 90))
        screen.blit(fuente.render(str(jugador.rect.h), True, COLORES.ALICEBLUE), (0, 120))

        pygame.draw.rect(screen, COLORES.AZURE1, fantasma.rect)
        fantasma.dibujar_hitbox(screen)
        pygame.draw.rect(screen, COLORES.AZURE1, jugador.rect)
        jugador.dibujar_hitbox(screen)
        if grupo_flechas:
            pygame.draw.rect(screen, COLORES.RED4, flecha.rect)
            flecha.dibujar_hitbox(screen)


    if fantasma.vivo:
        fantasma.dibujarse(screen)
        if grupo_flechas:
            fantasma.chequear_colisiones(flecha.rect)

    jugador.dibujarse(screen)

    grupo_flechas.update()
    grupo_flechas.draw(screen)
       
    pygame.display.flip()

pygame.quit()