import pygame
import os
import COLORES
import random
from FUNCIONES import *
from CONSTANTES import *
from Fantasma import Fantasma
from Jugador import Jugador
from Flecha import Flecha
from Cuchillo import Cuchillo

on = True

pygame.init()

# FRAMERATE

clock = pygame.time.Clock()
FPS = 60

# VENTANA
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Mi primera chamba")

# FUENTE Y TEXTOS
fuente = pygame.font.SysFont("Arial", 20)
texto_coordenadas = fuente.render("", True, COLORES.WHITE)


# VARIABLES DE JUEGO

GRAVEDAD = GRAVEDAD
coordenadas_click = [0, 0]

# VARIABLES DE JUGADOR

movimiento_izq = False
movimiento_der = False
ataque = False
lanzar_cuchillo = False

# grupos sprite

grupo_flechas = pygame.sprite.Group()
grupo_cuchillo = pygame.sprite.Group()

# IMAGEN FLECHA: la cargo aca para que sea siempre la misma y no cargarla cada vez que se dispara.

flecha_imagen = pygame.image.load(r"IMAGENES\PROPS\felcha.png").convert_alpha()
flecha_imagen = pygame.transform.scale_by(flecha_imagen, 1.6)

# ICONOS

icono_cuchillo = pygame.image.load(r"IMAGENES\PROPS\cuchillo\2.png").convert_alpha()
icono_cuchillo = pygame.transform.scale_by(icono_cuchillo, 2.5)

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

timer_15_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_15_segundos, 15000)

fantasma = Fantasma(570, 410, 2, 5, fuente)
jugador = Jugador(215, 425, 1.6, 5, fuente, 25)

texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)
debug_mode = False

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

        
        # mouse up
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                pass


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
            if evento.key == pygame.K_k:
                ataque = True
            if evento.key == pygame.K_l:
                lanzar_cuchillo = True



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

            if evento.key == pygame.K_l:
                lanzar_cuchillo = False
            
        
        # eventos de usuario
        elif evento.type == pygame.USEREVENT:
            if evento.type == timer_15_segundos:
                if fantasma.vivo is False:
                    #fantasma = Fantasma(random.randint(300,700), random.randint(0,300), 2, 5 , fuente)
                    pass
                


    ##############PANTALLA############################
    
    for fondo in lista_fondos:
        screen.blit(fondo, (0, 0))

    screen.blit(estructuras, (0,0))
    screen.blit(texto_coordenadas, POS_COORD)
    
    fantasma.actualizar()
    jugador.actualizar()
    
    if jugador.vivo:
        jugador.moverse(movimiento_izq, movimiento_der)



    if fantasma.vivo:
        if fantasma.accion_completa:
            fantasma.actualizar_accion(1)
    else:
        fantasma.actualizar_accion(3)

        
    #actualizar acciones . action handler
    if jugador.vivo:
        if ataque:
            jugador.actualizar_accion(3) # 3: ataque
            if jugador.accion_completa:
                flecha = Flecha((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion, flecha_imagen, jugador.flip)
                grupo_flechas.add(flecha) 
                ataque = False
        elif lanzar_cuchillo and jugador.cantidad_cuchillos > 0:
            cuchillo = Cuchillo((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion)
            grupo_cuchillo.add(cuchillo)
            lanzar_cuchillo = False
            jugador.cantidad_cuchillos -= 1
            texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)
                
        if jugador.en_aire:
            jugador.actualizar_accion(2) # 2: saltar
            if ataque:
                jugador.actualizar_accion(3) # 3: ataque
                if jugador.accion_completa:
                    flecha = Flecha((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion, flecha_imagen, jugador.flip)
                    grupo_flechas.add(flecha)
                    ataque = False
            elif lanzar_cuchillo and jugador.cantidad_cuchillos > 0:
                cuchillo = Cuchillo((jugador.rect.centerx + (35 * jugador.direccion)), (jugador.rect.centery + 7), jugador.direccion)
                grupo_cuchillo.add(cuchillo)
                lanzar_cuchillo = False
                jugador.cantidad_cuchillos -= 1
                texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)
                    

        elif movimiento_der or movimiento_izq:
           jugador.actualizar_accion(1) # 1: correr
        else:
            jugador.actualizar_accion(0) # 0: idle


    if debug_mode:
        screen.blit(jugador.rect_valor, (100, 0))
        screen.blit(fuente.render(str(jugador.rect.x), True, COLORES.ALICEBLUE), (0, 30))
        screen.blit(fuente.render(str(jugador.rect.y), True, COLORES.ALICEBLUE), (0, 60))
        screen.blit(fuente.render(str(jugador.rect.w), True, COLORES.ALICEBLUE), (0, 90))
        screen.blit(fuente.render(str(jugador.rect.h), True, COLORES.ALICEBLUE), (0, 120))

        #linea piso
        pygame.draw.line(screen, COLORES.YELLOW1, (0, PISO),(ANCHO_VENTANA, PISO))

        pygame.draw.rect(screen, COLORES.AZURE1, fantasma.rect)
        fantasma.dibujar_hitbox(screen)
        pygame.draw.rect(screen, COLORES.AZURE1, jugador.rect)
        jugador.dibujar_hitbox(screen)
        if grupo_flechas:
            pygame.draw.rect(screen, COLORES.RED4, flecha.rect)
            flecha.dibujar_hitbox(screen)
        if grupo_cuchillo:
            pygame.draw.rect(screen, COLORES.RED4, cuchillo.rect)
            cuchillo.dibujar_hitbox(screen)
            print(f"{cuchillo.rect.bottom}")

    fantasma.dibujarse(screen)
    jugador.dibujarse(screen)
    
    #jugador.imagen.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
    

    grupo_flechas.update(fantasma, grupo_flechas)
    grupo_cuchillo.update(fantasma, grupo_cuchillo)
    grupo_flechas.draw(screen)
    grupo_cuchillo.draw(screen)
    

    screen.blit(icono_cuchillo, (700, 10))
    screen.blit(texto_cantidad_cuchillos, (740, 10))
    
       
    pygame.display.flip()

pygame.quit()