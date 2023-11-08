import os
import pygame
import random
import COLORES
from FUNCIONES import *
from CONSTANTES import *
from Fantasma import Fantasma
from Jugador import Jugador
from Flecha import Flecha
from Cuchillo import Cuchillo
from Hongo import Hongo
from Rana import Rana

on = True

pygame.init()

# FRAMERATE

clock = pygame.time.Clock()
FPS = 60

# VENTANA

screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Mi primera duenda")
icono_ventana = pygame.image.load(r"IMAGENES\PERSONAJES\DUENDA\icono ventana.png").convert_alpha()
pygame.display.set_icon(icono_ventana)

# FUENTE Y TEXTOS

fuente = pygame.font.Font(r"IMAGENES\PROPS\monogram.ttf", 32)
texto_coordenadas = fuente.render("", True, COLORES.WHITE)


score = 0
texto_score = fuente.render(str(score), True, COLORES.WHITE)

lista_colores_score = [COLORES.GOLD1,COLORES.GOLD2 ,COLORES.GOLD3 ,COLORES.GOLD4 ,COLORES.GOLDENROD ,COLORES.GOLDENROD1 ,COLORES.GOLDENROD2 ,COLORES.GOLDENROD3 ,COLORES.GOLDENROD4]
indice_colores = 0

# VARIABLES DE JUEGO

GRAVEDAD = GRAVEDAD
coordenadas_click = [0, 0]
debug_mode = False

# VARIABLES DE JUGADOR

movimiento_izq = False
movimiento_der = False
ataque = False
lanzar_cuchillo = False

actualizador = 0
actualizador_rana = 0

# GRUPOS SPRITES

grupo_flechas = pygame.sprite.Group()
grupo_cuchillo = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()

# IMAGENES

fondo = pygame.image.load(r"IMAGENES\FONDO\fondo azul.png")
fondo = pygame.transform.scale_by(fondo, 2.1)

estructuras = pygame.image.load(r"IMAGENES\estructuras2.png").convert_alpha()
estructuras = pygame.transform.scale_by(estructuras, 1)

# IMAGEN FLECHA: la cargo aca para que sea siempre la misma y no cargarla cada vez que se dispara.

flecha_imagen = pygame.image.load(r"IMAGENES\PROPS\felcha.png").convert_alpha()
flecha_imagen = pygame.transform.scale_by(flecha_imagen, 1.6)

# ICONOS

icono_cuchillo = pygame.image.load(r"IMAGENES\PROPS\cuchillo\2.png").convert_alpha()
icono_cuchillo = pygame.transform.scale_by(icono_cuchillo, 2.5)

icono_duenda = pygame.image.load(r"IMAGENES\PERSONAJES\DUENDA\icono personaje.png").convert_alpha()
icono_duenda = pygame.transform.scale_by(icono_duenda, 1.8)

icono_corazones = pygame.image.load(r"IMAGENES\PROPS\corazon.png").convert_alpha()
icono_corazones = pygame.transform.scale_by(icono_corazones, 1.5)

barra_vida = pygame.image.load(r"IMAGENES\PROPS\barra.png").convert_alpha()
barra_vida = pygame.transform.scale_by(barra_vida, 1.28)

barra_cuchillo = pygame.image.load(r"IMAGENES\PROPS\barra.png").convert_alpha()
barra_cuchillo = pygame.transform.scale(barra_cuchillo, (icono_cuchillo.get_rect().w, icono_cuchillo.get_rect().h+6))

#EVENTOS USUARIO

timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 4000)

timer_colores = pygame.USEREVENT+1
pygame.time.set_timer(timer_colores, 120)


# INSTANCIAS

fantasma = Fantasma(570, 410, 2, 5, fuente)
jugador = Jugador(215, 425, 1.6, 5, fuente, 25)
hongo = Hongo(100, PISO, 2, 5, fuente)
rana = Rana(200, PISO, 2, 5, fuente)

grupo_enemigos.add(fantasma, hongo, rana)

texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)



while on:

    clock.tick(FPS)

    #######################EVENTOS###########################
    
    lista_eventos = pygame.event.get()

    score += 1
    
    for evento in lista_eventos:

        # quit
        if evento.type == pygame.QUIT:
            on = False
        
        # mouse click
        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            if evento.button == 1:

                coordenadas_click = list(evento.pos)
                texto_coordenadas = fuente.render(str(coordenadas_click), True, COLORES.WHITE)
                print(coordenadas_click)

        
        # mouse up
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                pass


        # presion tecla
        if evento.type == pygame.KEYDOWN:
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
        if evento.type == pygame.USEREVENT:
            if evento.type == timer_segundos:
                if fantasma.vivo is False:
                    #fantasma = Fantasma(random.randint(300,700), random.randint(0,300), 2, 5 , fuente)
                    pass
                if hongo.vivo:
                    hongo.actualizar_accion(actualizador)
                    actualizador += 1
                    if actualizador > 3:
                        actualizador = 0
                if rana.vivo:
                    rana.actualizar_accion(actualizador_rana)
                    actualizador_rana += 1
                    if actualizador_rana > 4:
                        actualizador_rana = 0

        if evento.type == pygame.USEREVENT+1:
            if indice_colores >= len(lista_colores_score) - 1:
                indice_colores = 0
            else:
                indice_colores += 1

    #####################PANTALLA############################
    
    
    screen.blit(fondo, (0, 0))
    screen.blit(estructuras, (0,0))
    screen.blit(icono_duenda, (0,0))
    screen.blit(texto_coordenadas, (0, 110))
    #screen.blit(barra_vida, (110, 0))
    screen.blit(icono_corazones, (100, 0))
    screen.blit(icono_corazones, (140, 0))
    screen.blit(icono_corazones, (180, 0))
    #screen.blit(barra_cuchillo, (110, 40))
    texto_score = fuente.render("SCORE " + str(score), True, lista_colores_score[indice_colores])
    screen.blit(texto_score, (340, 0))
    
    
    jugador.actualizar()

    for enemigo in grupo_enemigos:
        enemigo.actualizar()
    


    if jugador.vivo:
        jugador.moverse(movimiento_izq, movimiento_der)

    if fantasma.vivo:
        if fantasma.accion_completa:
            fantasma.actualizar_accion(1)
    else:
        fantasma.actualizar_accion(3)

        
    #actualizar acciones jugador . action handler
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
        screen.blit(jugador.rect_valor, (0, 260))
        screen.blit(fuente.render(str(jugador.rect.x), True, COLORES.YELLOW1), (0, 140))
        screen.blit(fuente.render(str(jugador.rect.y), True, COLORES.YELLOW1), (0, 170))
        screen.blit(fuente.render(str(jugador.rect.w), True, COLORES.YELLOW1), (0, 200))
        screen.blit(fuente.render(str(jugador.rect.h), True, COLORES.YELLOW1), (0, 230))

        #linea piso
        pygame.draw.line(screen, COLORES.YELLOW1, (0, PISO),(ANCHO_VENTANA, PISO))

        

        for enemigos in grupo_enemigos:
            pygame.draw.rect(screen, COLORES.AZURE1, enemigos.rect)
            enemigos.dibujar_hitbox(screen)

        for flechas in grupo_flechas:
            pygame.draw.rect(screen, COLORES.RED4, flechas.rect)
            flechas.dibujar_hitbox(screen)

        for cuchillos in grupo_cuchillo:
            pygame.draw.rect(screen, COLORES.RED4, cuchillos.rect)
            cuchillos.dibujar_hitbox(screen)
            print(f"{cuchillos.rect.bottom}")


    jugador.dibujarse(screen)
    #jugador.imagen.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT) 

    grupo_flechas.update(grupo_enemigos, grupo_flechas)
    grupo_cuchillo.update(grupo_enemigos, grupo_cuchillo)
    grupo_enemigos.update()
    
    grupo_flechas.draw(screen)
    grupo_cuchillo.draw(screen)
    grupo_enemigos.draw(screen)

    
    screen.blit(icono_cuchillo, (100, 42))
    screen.blit(texto_cantidad_cuchillos, (145, 47))
    
    pygame.display.flip()

pygame.quit()