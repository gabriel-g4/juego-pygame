import pygame
import COLORES
from FUNCIONES import *
from CONSTANTES import *
from Jugador import Jugador
from Rana import Rana
from Mundo import Mundo

on = True

pygame.init()
pygame.mixer.init()

# FRAMERATE
clock = pygame.time.Clock()
FPS = 60

# VENTANA
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Mi primera duenda")
icono_ventana = pygame.image.load(r"IMAGENES\PERSONAJES\DUENDA\icono ventana.png").convert_alpha()
pygame.display.set_icon(icono_ventana)

# AUDIO

pygame.mixer.music.load(r"SONIDO\musica menu.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

jugar_efecto = pygame.mixer.Sound(r"SONIDO\jugar.wav")
jugar_efecto.set_volume(0.2)

cuchillo_efecto = pygame.mixer.Sound(r"SONIDO\cuchillo.wav")
cuchillo_efecto.set_volume(0.5)

muerte_efecto = pygame.mixer.Sound(r"SONIDO\muerte duenda.wav")
muerte_efecto.set_volume(0.2)


# FUENTE Y TEXTOS
fuente = pygame.font.Font(r"IMAGENES\PROPS\monogram.ttf", 32)
fuente_titulo = pygame.font.Font(r"IMAGENES\PROPS\PIXEL-LI.TTF", 100)
fuente_subtitulos = pygame.font.Font(r"IMAGENES\PROPS\monogram.ttf", 80)


texto_titulo = fuente_titulo.render("Ranas asesinaS",True, COLORES.GREENYELLOW)
texto_coordenadas = fuente.render("", True, COLORES.WHITE)

score = 0
texto_score = fuente.render(str(score), True, COLORES.WHITE)
texto_muerte = fuente_titulo.render("Te moriste", True, COLORES.RED1)
texto_ingresar_nombre = fuente_subtitulos.render("Ingresa nombre", True, COLORES.RED1)
texto_presionar_enter = fuente_subtitulos.render("Presiona Enter..", True, COLORES.RED1)

lista_colores_score = [COLORES.GOLD1,COLORES.GOLD2 ,COLORES.GOLD3 ,COLORES.GOLD4 ,COLORES.GOLDENROD ,COLORES.GOLDENROD1 ,COLORES.GOLDENROD2 ,COLORES.GOLDENROD3 ,COLORES.GOLDENROD4]
indice_colores = 0

# VARIABLES DE JUEGO

iniciar_juego = False
bandera_leaderboards = False
escribir_nombre = False

ingreso = ""

botones_leader = False

nivel = 1
screen_scroll = 0
fondo_scroll = 0
GRAVEDAD = GRAVEDAD
coordenadas_click = [0, 0]
debug_mode = False
contador_segundos = 0

x_vidas = 100
x_cuchillos = 0


# VARIABLES DE JUGADOR
sonido_muerte = True
movimiento_izq = False
movimiento_der = False
ataque = False
lanzar_cuchillo = False

actualizador = 0
actualizador_rana = 0

# IMAGENES

fondo_menu = pygame.image.load(r"IMAGENES\FONDO\fondo azul simple.png").convert_alpha()
fondo_menu = pygame.transform.scale_by(fondo_menu, 2.8)
alpha = 128
beta = 150
fondo_menu.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

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

#CARGAR MAPA
mapa_nivel = cargar_mundo(nivel)
jugador = Jugador(215, 425, 1.6, 5, fuente, 15, score)
texto_cantidad_cuchillos = fuente.render(str(jugador.cantidad_cuchillos), True, COLORES.WHITE)
mundo = Mundo()
mundo.procesar_datos(mapa_nivel, lista_tiles, fuente, jugador, grupo_enemigos, grupo_decoracion, grupo_salida)


while on:

    clock.tick(FPS)

    #########################################################
    #######################EVENTOS###########################
    #########################################################
    
    lista_eventos = pygame.event.get()
    
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
                if botones_principal == True:
                    if rect_jugar.collidepoint(pos_mouse):
                        jugar_efecto.play()
                        iniciar_juego = True
                        bandera_leaderboards = False
                        escribir_nombre = False
                        botones_principal = False
                        
                    elif rect_leaderboards.collidepoint(pos_mouse):
                        pygame.mixer.music.load(r"SONIDO\musica leaderboard.wav")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                        
                        bandera_leaderboards = True
                        botones_principal = False
                        
                    elif rect_salir.collidepoint(pos_mouse):
                        on = False
                elif botones_leader == True:
                     if rect_atras.collidepoint(pos_mouse):
                        pygame.mixer.music.load(r"SONIDO\musica menu.wav")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                                                
                        iniciar_juego = False
                        bandera_leaderboards = False
                        botones_leader = False
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
                cuchillo_efecto.play()

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
            pass
               
        if evento.type == pygame.USEREVENT+1:
            if indice_colores >= len(lista_colores_score) - 1:
                indice_colores = 0
            else:
                indice_colores += 1
            
        if evento.type == pygame.USEREVENT:
            contador_segundos += 1


    if iniciar_juego == False and bandera_leaderboards == False:
        # Menu principal
        fondo_copia = fondo_menu.copy().convert_alpha()
        screen.blit(fondo_copia, (0,0))
        fondo_copia.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        pos_mouse = pygame.mouse.get_pos()
        texto_jugar = fuente_subtitulos.render("Jugar",True, COLORES.WHITE)
        texto_leaderboards = fuente_subtitulos.render("Leaderboards",True, COLORES.WHITE)
        texto_salir = fuente_subtitulos.render("Salir",True, COLORES.WHITE)
        rect_jugar = pygame.Rect(320, 250,texto_jugar.get_width(),  texto_jugar.get_height())
        rect_leaderboards = pygame.Rect(230, 350, texto_leaderboards.get_width(), texto_leaderboards.get_height())
        rect_salir = pygame.Rect(320, 450, texto_salir.get_width(), texto_salir.get_height())
        if rect_jugar.collidepoint(pos_mouse):
            texto_jugar = fuente_subtitulos.render("Jugar",True, COLORES.YELLOW1)
        elif rect_leaderboards.collidepoint(pos_mouse):
            texto_leaderboards = fuente_subtitulos.render("Leaderboards",True, COLORES.YELLOW1)
        elif rect_salir.collidepoint(pos_mouse):
            texto_salir = fuente_subtitulos.render("Salir",True, COLORES.YELLOW1)
        screen.blit(texto_titulo, (95, 40))
        screen.blit(texto_jugar, (320, 250))
        screen.blit(texto_leaderboards, (230, 350))
        screen.blit(texto_salir, (320, 450))
        
        botones_principal = True

        pygame.display.flip()

    elif bandera_leaderboards == True:
        
        screen.fill((32,73,68))
        screen.blit(lista_fondos[4], (0,0))
        pos_mouse = pygame.mouse.get_pos()
        texto_atras = fuente_subtitulos.render("Volver", True, COLORES.WHITE)
        rect_atras = pygame.Rect(320, 500, texto_atras.get_width(), texto_atras.get_height())
        if rect_atras.collidepoint(pos_mouse):
            texto_atras = fuente_subtitulos.render("Volver",True, COLORES.YELLOW1)
        if jugador.tiempo_muerte == 0:
            screen.blit(texto_atras, (320, 500))
            botones_leader = True
        

        lista_scores = seleccionar()
        y_leaders = 25
        for tupla in lista_scores:
            str_nombre = str(tupla[1])
            str_score = str(tupla[2])
            linea = fuente_subtitulos.render(f"{str_nombre:7}{str_score:10}",True, COLORES.GREENYELLOW)
            screen.blit(linea, (250, y_leaders))
            y_leaders += 100

        pygame.display.flip()
    
    elif escribir_nombre == True:

        screen.fill((32,73,68))
        screen.blit(lista_fondos[4], (0,0))
        screen.blit(texto_ingresar_nombre, (100, 100))
        screen.blit(texto_presionar_enter, (100, 500))

        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[0:-1]
                elif len(ingreso) < 3:
                    ingreso += evento.unicode
                
                if len(ingreso) == 3 and evento.key == pygame.K_RETURN:
                    insertar(str(ingreso), str(jugador.score))
                    botones_principal = False
                    bandera_leaderboards = True

        ingreso_txt = fuente_subtitulos.render(ingreso, True, COLORES.WHITE)
        screen.blit(ingreso_txt, (350,250))
        screen.blit(texto_score, (300, 350))
        

        pygame.display.flip()

        
        
    
    elif iniciar_juego == True:
        
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
        #screen.blit(texto_coordenadas, (0, 110))
        screen.blit(barra_vida, (85, -5))
        
        for vida in range(jugador.vida):
            screen.blit(cuadrado_vida, (x_vidas, 19))
            x_vidas += 26
        x_vidas = 134

        for cuchillo in range(jugador.cantidad_cuchillos):
            screen.blit(icono_cuchillo, (x_cuchillos, 50))
            x_cuchillos += 10
        x_cuchillos = 80

        texto_score = fuente.render("SCORE " + str(jugador.score), True, lista_colores_score[indice_colores])
        screen.blit(texto_score, (650, 33))
        texto_segundos = fuente.render("TIEMPO " + str(contador_segundos), True, COLORES.WHITE)
        screen.blit(texto_segundos, (650, 3))


        ###########ACCIONES##############

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

        # chequear si gano, si es asi resetea variables y cambia de nivel
        for salida in grupo_salida:
            salida.update(screen_scroll)
            nuevo_nivel = salida.comprobar_finalizacion(jugador)
            if nuevo_nivel:
                nivel += 1
                jugador.vida = 3
                if nivel > 3:
                    escribir_nombre =  True
                    break
                mapa_nivel = cargar_mundo(nivel)
                fondo_scroll = 0
                screen_scroll = 0
                for enemigo in grupo_enemigos:
                    enemigo.kill()
                salida.kill()
                mundo = Mundo()
                mundo.procesar_datos(mapa_nivel, lista_tiles, fuente, jugador, grupo_enemigos, grupo_decoracion, grupo_salida)
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

        if not jugador.vivo:
            if sonido_muerte:
                muerte_efecto.play()
                sonido_muerte = False
            if jugador.tiempo_muerte > 150:
                screen.fill((0,0,0))
                screen.blit(texto_muerte, (200,260))
                if jugador.tiempo_muerte > 300:
                    pygame.mixer.music.load(r"SONIDO\musica leaderboard.wav")
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    escribir_nombre = True
                    texto_score = fuente_subtitulos.render(f"SCORE: {str(jugador.score)}", True, COLORES.RED1)
        
        pygame.display.flip()

pygame.quit()