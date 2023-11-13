import pygame
import COLORES
from FUNCIONES import *
from CONSTANTES import *
from Fantasma import Fantasma
from Jugador import Jugador
from Hongo import Hongo
from Rana import Rana
from Mundo import Mundo

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
nivel = 0
screen_scroll = 0
fondo_scroll = 0
GRAVEDAD = GRAVEDAD
coordenadas_click = [0, 0]
debug_mode = False
contador_segundos = 0

x_vidas = 100
x_cuchillos = 0

# VARIABLES DE JUGADOR
movimiento_izq = False
movimiento_der = False
ataque = False
lanzar_cuchillo = False

actualizador = 0
actualizador_rana = 0

# IMAGENES
lista_fondos = []
for i in range(1, 7):
    fondo = pygame.image.load(f"IMAGENES/FONDO/plx-{i}.png").convert_alpha()
    if i != 6 and i != 5:
        fondo = pygame.transform.scale_by(fondo, 2.5)
    else:
        fondo = pygame.transform.scale_by(fondo, 2.8)
    lista_fondos.append(fondo)

# GUARDAR TILES EN LISTA
lista_tiles = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f"IMAGENES\\TILES\\{i}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    lista_tiles.append(img)

# IMAGEN FLECHA: la cargo aca para que sea siempre la misma y no cargarla cada vez que se dispara.
flecha_imagen = pygame.image.load(r"IMAGENES\PROPS\felcha.png").convert_alpha()
flecha_imagen = pygame.transform.scale_by(flecha_imagen, 1.6)

# ICONOS
icono_cuchillo = pygame.image.load(r"IMAGENES\PROPS\cuchillo\2.png").convert_alpha()
icono_cuchillo = pygame.transform.scale_by(icono_cuchillo, 1.8)

icono_duenda = pygame.image.load(r"IMAGENES\PERSONAJES\DUENDA\icono personaje.png").convert_alpha()
icono_duenda = pygame.transform.scale_by(icono_duenda, 1.5)

icono_corazones = pygame.image.load(r"IMAGENES\PROPS\corazon.png").convert_alpha()
icono_corazones = pygame.transform.scale_by(icono_corazones, 1.3)

barra_vida = pygame.image.load(r"IMAGENES\PROPS\barra de vida.png").convert_alpha()
barra_vida = pygame.transform.scale_by(barra_vida, 0.8)

cuadrado_vida = pygame.image.load(r"IMAGENES\PROPS\cuadrado vida.png").convert_alpha()
cuadrado_vida = pygame.transform.scale_by(cuadrado_vida, 0.80)


#CARGAR MAPA
mapa_nivel = []
with open(f"NIVELES\level{nivel}_data.csv", "r") as archivo:
    for linea in archivo:
        linea = linea.replace("\n", "")
        linea = linea.split(",")

        for i in range(len(linea)):
            linea[i] = int(linea[i])

        mapa_nivel.append(linea)

#EVENTOS USUARIO
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 1000)

timer_colores = pygame.USEREVENT+1
pygame.time.set_timer(timer_colores, 120)

timer_bichos = pygame.USEREVENT+2
pygame.time.set_timer(timer_bichos, 4000)


# GRUPOS SPRITES
grupo_flechas = pygame.sprite.Group()
grupo_cuchillo = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_decoracion = pygame.sprite.Group()
grupo_salida = pygame.sprite.Group()

# INSTANCIAS
jugador = Jugador(215, 425, 1.6, 5, fuente, 15)
fantasma = Fantasma(570, 410, 2, 5, fuente)
hongo = Hongo(100, PISO, 2, 5, fuente)
rana = Rana(330, 520, 2, 2, fuente, jugador)

grupo_enemigos.add(fantasma, hongo, rana)
texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)

mundo = Mundo()
mundo.procesar_datos(mapa_nivel, lista_tiles, fuente, jugador, grupo_enemigos, grupo_decoracion, grupo_salida)


while on:

    clock.tick(FPS)

    #########################################################
    #######################EVENTOS###########################
    #########################################################
    
    lista_eventos = pygame.event.get()

    score += 2
    
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
        if evento.type == pygame.USEREVENT+2:
            if evento.type == timer_bichos:
                if fantasma.vivo is False:
                    #fantasma = Fantasma(random.randint(300,700), random.randint(0,300), 2, 5 , fuente)
                    pass
                if hongo.vivo:
                    hongo.actualizar_accion(actualizador)
                    actualizador += 1
                    if actualizador > 3:
                        actualizador = 0
                    
        if evento.type == pygame.USEREVENT+1:
            if indice_colores >= len(lista_colores_score) - 1:
                indice_colores = 0
            else:
                indice_colores += 1
            
        if evento.type == pygame.USEREVENT:
            contador_segundos += 1


    #########################################################
    #####################PANTALLA############################
    #########################################################

    for i in range(3):
        parallax = 0.5
        for fondo in lista_fondos:
            screen.blit(fondo, ((i * TAMAÑO_IMAGEN) - fondo_scroll * parallax, 0))
            parallax += 0.1

    # dibujar tiles
    mundo.dibujar(screen, screen_scroll)
    screen.blit(icono_duenda, (0,0))
    screen.blit(texto_coordenadas, (0, 110))
    screen.blit(barra_vida, (85, -5))
    
    for vida in range(jugador.vida):
        screen.blit(cuadrado_vida, (x_vidas, 19))
        x_vidas += 26
    x_vidas = 134

    for cuchillo in range(jugador.cantidad_cuchillos):
        screen.blit(icono_cuchillo, (x_cuchillos, 50))
        x_cuchillos += 10
    x_cuchillos = 80

    texto_score = fuente.render("SCORE " + str(score), True, lista_colores_score[indice_colores])
    screen.blit(texto_score, (650, 33))
    texto_segundos = fuente.render("TIEMPO " + str(contador_segundos), True, COLORES.WHITE)
    screen.blit(texto_segundos, (650, 3))


    ###########ACCIONES##############

    if fantasma.vivo:
        if fantasma.accion_completa:
            fantasma.actualizar_accion(1)
    else:
        fantasma.actualizar_accion(3)


    jugador.actualizar()
    #action handler
    screen_scroll, fondo_scroll, texto_cantidad_cuchillos, ataque, lanzar_cuchillo = jugador.action_handler(movimiento_izq, movimiento_der, mundo, grupo_flechas, grupo_cuchillo, fondo_scroll, flecha_imagen, ataque, lanzar_cuchillo)

    if debug_mode:
        screen.blit(jugador.rect_valor, (0, 260))
        screen.blit(fuente.render(str(jugador.rect.x), True, COLORES.YELLOW1), (0, 140))
        screen.blit(fuente.render(str(jugador.rect.y), True, COLORES.YELLOW1), (0, 170))
        screen.blit(fuente.render(str(jugador.rect.w), True, COLORES.YELLOW1), (0, 200))
        screen.blit(fuente.render(str(jugador.rect.h), True, COLORES.YELLOW1), (0, 230))

        for rana in grupo_enemigos:
            if type(rana) == Rana:
                pygame.draw.rect(screen, COLORES.GREEN, rana.rect_vision)



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
        
        for proyectil in grupo_proyectiles:
            pygame.draw.rect(screen, COLORES.RED4, proyectil.rect)
            proyectil.dibujar_hitbox(screen)
        
        pygame.draw.rect(screen, COLORES.AZURE1, jugador.rect)
        jugador.dibujar_hitbox(screen)

    grupo_decoracion.update(screen_scroll)
    grupo_decoracion.draw(screen)

    grupo_salida.update(screen_scroll)
    grupo_salida.draw(screen)
    
    jugador.dibujarse(screen)
    
    for enemigo in grupo_enemigos:
        if type(enemigo) != Rana:
            enemigo.actualizar()
            enemigo.draw(screen)
        else:
            enemigo.inteligencia(mundo)
            enemigo.actualizar(grupo_proyectiles)
            enemigo.draw(screen, screen_scroll)

    grupo_flechas.update(grupo_enemigos, grupo_flechas, mundo, screen_scroll)
    grupo_cuchillo.update(grupo_enemigos, grupo_cuchillo, mundo, screen_scroll)
    grupo_enemigos.update()
    grupo_proyectiles.update(jugador, grupo_proyectiles, screen_scroll, mundo)
    
    grupo_flechas.draw(screen)
    grupo_cuchillo.draw(screen)
    grupo_proyectiles.draw(screen)
    
    pygame.display.flip()

pygame.quit()